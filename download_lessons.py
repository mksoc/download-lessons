from selenium import webdriver
import subprocess
import sys

#--- Function definitions ---
def open_page(link):
    print('Opening browser and course page...')
    driver.get(link)
    try:
        assert "Lezione" in driver.title
    except AssertionError:
        print('ERROR. Wrong page title. Check provided link.')
        raise
        
def get_lesson_list():
    lessons = driver.find_elements_by_partial_link_text('Lezioni')
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

def get_download_links(list):
    urls = []
    for i in range(len(list)):
        print('Getting download link of lesson {} of {}'.format(i+1, len(list)))
        driver.get(list[i])
        video = driver.find_element_by_id('video1')
        urls.append(video.get_attribute('href'))
    return urls
    
def download(list, path):
    for i in range(len(list)):
        print('Downloading lesson {} of {}'.format(i+1, len(list)))
        command = """bash -c "wget --trust-server-names -P %s '%s'" """ % (path, list[i])
        subprocess.call(command, shell=True)
    print('All downloads completed successfully!')
#--- End function definitions ---

# Define the url of the course and output directory
course_url = 'https://elearning.polito.it/gadgets/video/template_video.php?utente=S213513&inc=202712&data=220420171728&token=926189389C4432FEAB407397FCB6A60B'
output_dir = '/mnt/d/videolezioni/misure'
phantomjs_dir = r'D:\Applicazioni\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe'

print('Script starting. Press Ctrl + C to cancel.')

driver = webdriver.PhantomJS(phantomjs_dir)

try:
    open_page(course_url)
    lessons = get_lesson_list()
except:
    print('Script execution was not successful.')
    sys.exit(1)

lesson_urls = get_lesson_links(lessons)
download_urls = get_download_links(lesson_urls)
download(download_urls, output_dir)