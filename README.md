# StyleTransformerGANs
## Final project to Deep Learning School. Style Trasformer via telegram bot.
## You can check how this works in demo notebooks
### About
Bot's name: **@styletransferjune2020bot**, try it! 

UPD: It's over cause my AWS free month is over :)

When you want to impose some kind of style on an image, you can use just such a bot.
The bottom line is simple: upload an image with content, upload a style, the bot itself creates a connected image.
To better understand what is at stake, take a look at a few examples:
![visocky](https://github.com/germanjke/StyleTransformerGANs/blob/master/examples/visocky_readme.png)
![mayakovsky](https://github.com/germanjke/StyleTransformerGANs/blob/master/examples/mayakovsky_readme.png)
![gagarin](https://github.com/germanjke/StyleTransformerGANs/blob/master/examples/gagarin_readme.png)

This project includes three main parts:
1. StyleTransform Network
2. Telegram Bot
3. Deploying (via AWS)

#### StyleTransform Network
[Multi-Style-Transfer model](https://github.com/zhanghang1989/PyTorch-Multi-Style-Transfer) by [Hang Zhang](https://github.com/zhanghang1989) was a key point in this project. You can check [arxiv](https://arxiv.org/pdf/1703.06953.pdf) about Multi-style Generative Network for Real-time Transfer.

#### Telegram Bot
Bot using [aiogram](https://docs.aiogram.dev/en/latest/) library for Python.
To better understand how it's works, take a look at some actions:

First, you choose content image, second - style image. 

<img src="https://github.com/germanjke/StyleTransformerGANs/blob/master/examples/2.jpg" width="300">

Then, you need to choose quality. The lower the quality, the less time it takes to process. High quality takes about 15-30 seconds.

<img src="https://github.com/germanjke/StyleTransformerGANs/blob/master/examples/4.png">

Bot returns you result image and type /continue command.

<img src="https://github.com/germanjke/StyleTransformerGANs/blob/master/examples/3.jpg" width="300">

You can use /help command to see some help.

<img src="https://github.com/germanjke/StyleTransformerGANs/blob/master/examples/1.jpg" width="300">

#### Deploying (via AWS)
Bot loaded using [AWS](https://aws.amazon.com/), [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/) and [WinSCP](https://winscp.net/eng/docs/start). First you need to create a server using AWS. Then, using PuTTY, we start the server on Ubuntu. Using WinSCP, we run this on Windows.
