import logging
import gc

from aiogram import Bot, Dispatcher, executor, types

from network import *  # Import architecture
from help_functions import *  # Import help functions


# Set API_TOKEN. You must have your own.
API_TOKEN = '' # TYPE IT HERE! 

# Configure logging.
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher.
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Initialize the net.
style_model = Net(ngf=128)
style_model.load_state_dict(torch.load('pretrained.model'), False)

# Initializing the flag to distinguish between images content and style.
flag = True
# Initializing flags to check for images.
content_flag = False
style_flag = False


def transform(content_root, style_root, im_size):
    """Function for image transformation."""
    content_image = tensor_load_rgbimage(content_root, size=im_size,
                                         keep_asp=True).unsqueeze(0)
    style = tensor_load_rgbimage(style_root, size=im_size).unsqueeze(0)
    style = preprocess_batch(style)
    style_v = Variable(style)
    content_image = Variable(preprocess_batch(content_image))
    style_model.setTarget(style_v)
    output = style_model(content_image)
    tensor_save_bgrimage(output.data[0], 'result.jpg', False)

    # Clear the RAM.
    del content_image
    del style
    del style_v
    del output
    torch.cuda.empty_cache()

    gc.collect()


@dp.message_handler(commands=['test'])
async def test(message: types.Message):
    """Test function."""
    await message.answer(text='It works!')


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    """
    Outputs a small instruction when the corresponding command is received.
    """
    await message.answer(text="This bot will helps you making style transformations, "
                              "Load photo with your content first. "
                              "Then, load photo with style "
                              "You will be get joint image. "
                              "To check the code and contact me enter /about command."
                              " Let me show you some examples to make you understand.  ")
    with open('visocky_readme.png','rb') as photo:
        await message.reply_photo(photo, caption = 'Visocky and Van Gogh')
    with open('mayakovsky_readme.png','rb') as photo:
        await message.reply_photo(photo, caption='Mayakovsky and Van Gogh')
    with open('gagarin_readme.png','rb') as photo:
        await message.reply_photo(photo,caption='Gagarin and Van Gogh')

@dp.message_handler(content_types=['photo'])
async def photo_processing(message):
    """
    Triggered when the user sends an image and saves it for further processing.
    """

    global flag
    global content_flag
    global style_flag

    # The bot is waiting for a picture with content from the user.
    if flag:
        await message.photo[-1].download('content.jpg')
        await message.answer(text='Got content image.'
                                  ' Send me style image please. '
                                  'the /back command to choose '
                                  'a different content image.')
        flag = False
        content_flag = True  # Now the bot knows that the content image exists.

    # The bot is waiting for a picture with style from the user.
    else:
        await message.photo[-1].download('style.jpg')
        await message.answer(text='Got style image'
                                  ' the /back command to choose '
                                  'a different style image.'
                                  ' Enter /continue command to launch transfering. ')
        flag = True
        style_flag = True  # Now the bot knows that the style image exists.


@dp.message_handler(commands=['back'])
async def photo_processing(message: types.Message):
    """Allows the user to select a different image with content or style."""

    global flag
    global content_flag

    # Let's make sure that there is something to cancel.
    if not content_flag:
        await message.answer(text="Content image not uploaded.")
        return

    if flag:
        flag = False
    else:
        flag = True
    await message.answer(text='Successfully!')


@dp.message_handler(commands=['about'])
async def creator(message: types.Message):
    """Displays information about the bot's Creator."""
    link = 'https://https://github.com/germanjke/StyleTransformerGANs'
    link2 = '@logisticregression'
    await message.answer(text=f'Bot created for final Deep Learning School by MIPT project .\
                              \nLink to github repo: {link}, contact me: {link2}')


@dp.message_handler(commands=['continue'])
async def contin(message: types.Message):
    """Preparing for image processing."""

    # Let's make sure that the user has added both images.
    if not (content_flag * style_flag):  # Conjunction
        await message.answer(text="Upload both images please.")
        return

    # Adding answer options.
    res = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True)
    res.add(types.KeyboardButton(text="Bad quality, low time"))
    res.add(types.KeyboardButton(text="Medium quality, medium time"))
    res.add(types.KeyboardButton(text="Good quality, bigger time"))

    await message.answer(text="The choice of quality is yours."
                              " Remember, the lower the quality (resolution), the faster you get the picture. ", reply_markup=res)


@dp.message_handler(lambda message: message.text in ("Bad quality, low time", "Medium quality, medium time", "Good quality, bigger time"))
async def processing(message: types.Message):
    """Image processing depending on the selected quality."""

    if message.text == 'Bad quality, low time':
        image_size = 128
    elif message.text == 'Medium quality, medium time':
        image_size = 256
    else:
        image_size = 300

    await message.answer(text='Style transfering starts. '
                              'Wait a bit.',
                         reply_markup=types.ReplyKeyboardRemove())
    transform('content.jpg', 'style.jpg', image_size)
    with open('result.jpg', 'rb') as file:
        await message.answer_photo(file, caption='Work is done!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
