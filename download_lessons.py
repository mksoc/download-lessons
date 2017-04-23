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
    except AssertionError:
        print('ERROR. No lesson found. Check provided link.')
        raise
#--- End function definitions ---

# Define the url of the course and output directory
course_url = 'https://elearning.polito.it/gadgets/video/template_video.php?utente=S213513&inc=202712&data=220420171728&token=926189389C4432FEAB407397FCB6A60B'
output_dir = '/mnt/d/videolezioni/misure'
phantomjs_dir = r'D:\Applicazioni\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe'

print('Script starting. Press Ctrl + C to cancel.')

driver = webdriver.PhantomJS(phantomjs_dir)

try:
    open_page(course_url)
    get_lesson_list()
except:
    print('Script execution was not successful.')
    sys.exit(1)

    
# Extract the links of the lessons
print('Getting lessons links...')
lesson_urls = []
for item in lessons:
    lesson_urls.append(item.get_attribute('href'))
    
# Open each link and extract the download url
download_urls = []
for i in range(len(lesson_urls)):
    print('Getting download link of lesson {} of {}'.format(i+1, len(lesson_urls)))
    driver.get(lesson_urls[i])
    video = driver.find_element_by_id('video1')
    download_urls.append(video.get_attribute('href'))

# Download files to output_dir
for i in range(len(download_urls)):
    print('Downloading lesson {} of {}'.format(i+1, len(download_urls)))
    command = """bash -c "wget --trust-server-names -P %s '%s'" """ % (output_dir, download_urls[i])
    subprocess.call(command, shell=True)

print('All downloads completed successfully!')