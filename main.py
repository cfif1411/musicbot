import os
import telebot
from pytube import YouTube

from bs4 import BeautifulSoup
from selenium import webdriver

bot = telebot.TeleBot('5536743093:AAGhb25SbA0iVfc1X5TjGbk1si83W-81q7c')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привіт)')


@bot.message_handler()
def download(message):
    print('Start app Download music!')
    link = search_text(message)
    try:
        yt = YouTube(link)
    except:
        print("App is not download!")

    print(yt.title)

    iTagHighestResVideo = yt.streams.filter(progressive="True").get_highest_resolution().itag

    try:
        bot.send_message(message.chat.id, 'Start download music!')
        yt.streams.get_by_itag(iTagHighestResVideo).download(output_path='C:/Users/Sasha Shpakovskiy/Desktop',
                                                             filename=f'{yt.title}.mp3')
    except:
        print('This music is not download!')
    print(f'{yt.title} download is pc!')

    try:
        bot.send_message(message.chat.id, 'Start send message!')
        audio = open(f'C:/Users/Sasha Shpakovskiy/Desktop/{yt.title}.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)
        audio.close()
        os.remove(path=f'C:/Users/Sasha Shpakovskiy/Desktop/{yt.title}.mp3')


    except:
        print('Do not download audio!')


def search_text(text):
    if 'http' not in text.text:

        driver = webdriver.Chrome(
            executable_path='C://Users//Sasha Shpakovskiy//PycharmProjects//telegram_bot//selenium brouser//chromedriver.exe')
        url = f'https://www.youtube.com/results?search_query={"+".join(text.text.split())}'
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        video_url = soup.find('a', id='video-title').get('href')
        return video_url
    elif 'http' in text.text:
        return text.text


bot.polling(non_stop=True)
