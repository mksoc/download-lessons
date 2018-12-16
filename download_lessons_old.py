#!/usr/bin/python3

from selenium import webdriver
import subprocess
import argparse


def open_page(driver, link):
    print('Opening browser and course page...')
    driver.get(link)
    try:
        assert "Lezione" in driver.title
    except AssertionError:
        print('ERROR. Wrong page title. Check provided link.')
        raise


def get_lesson_list(driver):
    lessons = driver.find_elements_by_partial_link_text('Lezione')
    try:
        assert len(lessons) > 0
        print('Found {} lessons.'.format(len(lessons)))
        return lessons
    except AssertionError:
        print('ERROR. No lesson found. Check provided link.')
        raise


def get_lesson_links(list):
    print('Getting lessons links...')
    urls = []
    for item in list:
        urls.append(item.get_attribute('href'))
    return urls


def get_download_links(driver, list):
    urls = []
    for i in range(len(list)):
        print('Getting download link of lesson {} of {}'.format(i + 1, len(list)))
        driver.get(list[i])
        video = driver.find_element_by_id('video1')
        urls.append(video.get_attribute('href'))
    return urls


def download(list, path):
    for i in range(len(list)):
        print('Downloading lesson {} of {}'.format(i + 1, len(list)))
        command = """bash -c "wget --trust-server-names -P %s '%s'" """ % (
            path, list[i])
        subprocess.call(command, shell=True)
    print('All downloads completed successfully!')


def main():
    parser = argparse.ArgumentParser(description='Automatically download lessons from Portale della Didattica')
    parser.add_argument('url', help='course URL')
    parser.add_argument('output_dir', help='output directory')
    args = parser.parse_args()

    print('Script starting. Press Ctrl + C to cancel.')

    browser = webdriver.Firefox()
    open_page(browser, args.url)
    lessons = get_lesson_list(browser)

    lesson_urls = get_lesson_links(lessons)
    download_urls = get_download_links(browser, lesson_urls)
    download(download_urls, args.output_dir)


if __name__ == "__main__":
    main()
