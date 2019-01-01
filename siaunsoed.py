from bs4 import BeautifulSoup
import cookielib
import urllib2
import mechanize
import random

browser = mechanize.Browser()

cookiejar = cookielib.LWPCookieJar()
browser.set_cookiejar(cookiejar)

browser.set_handle_equiv(True) 
browser.set_handle_gzip(True) 
browser.set_handle_redirect(True) 
browser.set_handle_referer(True) 
browser.set_handle_robots(False) 

browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1) 

browser.addheaders = [('User-agent', 'Mozilla/5.0')]

browser.open('https://akademik.unsoed.ac.id/index.php?r=site/login')
browser.select_form(nr=0)

browser["LoginForm[username]"] = raw_input('masukkan NIM Anda          : ')
browser["LoginForm[password]"] = raw_input('Masukkan password SIA Anda : ')

res = browser.submit()

print "Berhasil melakukan login pada SIA Unsoed!"

url = browser.open('https://akademik.unsoed.ac.id/index.php?r=masterkuispembelajaran/viewbynim')

html_tabel_matkul = url.read()
matkul_soup = BeautifulSoup(html_tabel_matkul, 'html.parser')

tabel_matkul = matkul_soup.find("table")

nama_matkul = [item('td')[1].text for item in tabel_matkul.find_all('tr')[1:]]
link_matkul = [link.get('href') for link in tabel_matkul.find_all('a')]

endpoint = 'https://akademik.unsoed.ac.id'

for i in range(len(link_matkul)):
    url = browser.open(endpoint + link_matkul[i])
    browser.select_form(nr=0)

    html_kuis = url.read()
    kuis_soup = BeautifulSoup(html_kuis, 'html.parser')

    idkuis = int(kuis_soup.find('input').get('id').split('_')[1])

    for i in range(15):
        part1 = 'Kuispembelajaran['
        part2 = '][jawabankuis]'
        control = browser.find_control(name= part1 + str(idkuis + i) + part2, nr=1)
        control.value = [str(random.randint(2, 4))]

    browser.find_control(name='Masterkuispembelajaran[saran]').value = "Semoga kedepannya dapat menjadi lebih baik lagi"

    browser.submit()

    print('Kuisioner mata kuliah ' + nama_matkul[i] + ' berhasil diisi!')