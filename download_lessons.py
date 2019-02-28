#!/usr/bin/python3

from selenium import webdriver, common
import parser
import os
import urllib.request

args = parser.setup_parser()

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

# try closing something obscuring the course link
try:
    driver.find_element_by_partial_link_text(args.course).click()
except common.exceptions.ElementClickInterceptedException:
    driver.find_element_by_link_text('Non mostrare più per oggi').click()
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
if args.newer:
    if any([('lez' in item) and ('mp4' in item) for item in os.listdir(args.output_dir)]):
        latest = max([int(item.split('_')[-1].split('.')[0]) for item in os.listdir(args.output_dir) if 'mp4' in item])
        urls = [item.get_attribute('href') for item in lessons[latest:]]
elif args.latest:
    urls = [lessons[-1].get_attribute('href')]
else:
    urls = [item.get_attribute('href') for item in lessons]

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
    actual_url = urllib.request.urlopen(item).geturl()  # follow redirect to actual file
    with urllib.request.urlopen(actual_url) as response, open('{}/{}'.format(args.output_dir, actual_url.split('/')[-1]), 'wb') as out_file:
        out_file.write(response.read())
print('All downloads completed successfully!')

# clean up
driver.close()
