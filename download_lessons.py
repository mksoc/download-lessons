#!/usr/bin/python3

from selenium import webdriver, common
import subprocess
import argparse

# define cmd line arguments
parser = argparse.ArgumentParser(description='Automatically download lessons from Portale della Didattica')
parser.add_argument('-u', dest='username', help='Polito username', required=True)
parser.add_argument('-p', dest='password', help='Polito password', required=True)
parser.add_argument('-t', '--max-wait', dest='max_wait', type=int, default=10, help='number of seconds to wait for page loading (default 10)')
parser.add_argument('-b', '--begin', type=int, default=1, help='lesson number to begin downloads (default 1)')
parser.add_argument('-e', '--end', type=int, help='lesson number to end downloads (default last one)')
parser.add_argument('course', help='exact name of the course in the Portale')
parser.add_argument('output_dir', help='output directory')
args = parser.parse_args()

# open browser on login page
print('Opening browser towards lessons page...')
driver = webdriver.Firefox(service_log_path='/dev/null')
driver.implicitly_wait(args.max_wait)  # seconds to wait for page loading on each click

driver.get('https://idp.polito.it/idp/x509mixed-login')
driver.find_element_by_id('j_username').send_keys(args.username)
driver.find_element_by_id('j_password').send_keys(args.password)
driver.find_element_by_id('usernamepassword').click()

try:
    driver.find_element_by_link_text('Portale della Didattica').click()
except common.exceptions.NoSuchElementException:   
    print('Error. Could not find Portale della Didattica. Check your login info or that Polito servers are running correctly.')

driver.find_element_by_partial_link_text(args.course).click()

driver.find_element_by_partial_link_text('Accedi al materiale e-learning').click()
try:
    driver.find_element_by_partial_link_text('Lezioni Online').click()
except common.exceptions.NoSuchElementException:
    driver.find_element_by_partial_link_text('Lessons').click()

# get lessons list
print('Getting lessons list...')
lessons = driver.find_elements_by_partial_link_text('Lezione')
print('  Found {} lessons.'.format(len(lessons)))

print('Getting lessons links...')
if not args.end:
    urls = [item.get_attribute('href') for item in lessons[args.begin - 1:]]
else:
    urls = [item.get_attribute('href') for item in lessons[args.begin - 1:args.end - 1]]
print('  Will download {} lessons.'.format(len(urls)))

# get download links
download_urls = []
for item in urls:
    print('Getting download link of lesson {} of {}...'.format(urls.index(item) + 1, len(urls)))
    driver.get(item)
    download_urls.append(driver.find_element_by_id('video1').get_attribute('href'))

# download lessons
for item in download_urls:
    print('Downloading lesson {} of {}'.format(download_urls.index(item) + 1, len(download_urls)))
    command = """bash -c "wget --trust-server-names -P %s '%s'" """ % (args.output_dir, item)
    subprocess.call(command, shell=True)
print('All downloads completed successfully!')

# clean up
driver.close()
