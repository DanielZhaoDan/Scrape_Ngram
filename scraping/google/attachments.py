# -*- coding: utf-8 -*-
from scraping.utils import get_attachments, post_request_html, write_excel
import re

cookie = '__utma=231532751.117749773.1601608000.1601608992.1601608992.1; __utmb=231532751.0.10.1601608992; __utmc=231532751; __utmz=231532751.1601608992.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); GA_XSRF_TOKEN=AO6Y7m9AzsUFDGU2E7K6jHNKl4-0p-7Gvw:1601609079053; _ga=GA1.3-2.117749773.1601608000; _gid=GA1.3-2.458288583.1601608000; SEARCH_SAMESITE=CgQIh5AB; CONSENT=YES+SG.en+20180429-14-0; ANID=AHWqTUllU28tBoAV12uKiCtH3D5X1kAXClMr9H6bb_E494aeYmg-AMON00z8EVPK; 1P_JAR=2020-10-01-10; _gid=GA1.3.458288583.1601608000; SID=2Adjk9UOUOKvgn-IX1lD70-0LUL8GQRXNLqAfKWyLjaPE_IinYllYFc9XpFPVEmQ9u_Ivg.; __Secure-3PSID=2Adjk9UOUOKvgn-IX1lD70-0LUL8GQRXNLqAfKWyLjaPE_IiNIdBNCGBZWAXsGv64WiMBQ.; HSID=AfwM6kd2FQ-hCPZGo; SSID=Ar6hmxIjKeUySyYsn; APISID=36mJlPXLyVIRp6tG/Aa1f722gcLfAmnckc; SAPISID=2aFcz5oYBdtG5u51/AzPZVkG0TKFhMyODC; __Secure-3PAPISID=2aFcz5oYBdtG5u51/AzPZVkG0TKFhMyODC; NID=204=ry24gXpIyCLTYaRdu87zOI-oTAyZbaoKb4SLCywLmDFvr6sSwzXpNbK5L_ZeDEygIGURo5GcZLZ-n22vLKlJvuINoXVj7FaWdmLNQSdPY5lEkdtDtAML5OLY34HirJps6bwh0vFY4eYnTyPxRnUYF_7Y5zHdwQpQKtjXndzGFwJCzk3T2mZnS_FeZrWinS7_3P607lMOarPbL6qyPOBBDXHDuzglEGUVHJXhN_C5M0FPWuuMmISVNjijXMG5OWFmwtRTrhuUruaC938; S=analytics-realtime-frontend=LQQS0JehYfQBFggK94zpSJEwD5x9Bs7J; _gat_UA-60390233-4=1; _gat=1; _gat_ta=1; _gat_tw=1; _ga=GA1.1.117749773.1601608000; _ga_X6LMX9VR0Y=GS1.1.1601608002.1.1.1601609281.0; SIDCC=AJi4QfHCXzm9MOYuoI-UWr08hqRVwNP9n1OhrJgGagLrQIRmf99CcQ5pKiJmwYGKYg242K2LFbI; __Secure-3PSIDCC=AJi4QfGr2FQt2xDd35RxQl53a4_MAQNB3LpCXZc5oEtMVBp74bX74jz_Z7ou3wbwy5dmnrrlDg'
x_token = 'AO6Y7m9KjxqcxeilagJ3EA0NjOhu8PYsXg:1601609083769'

sheet_p = [['Pages', 'Previous Page Path', 'Page Views', '%Page Views']]
sheet_n = [['Pages', 'Next Page Path', 'Page Views', '%Page Views']]

# a116178497w86333592p89585249


def prepare_url():
    urls = [
        [
            '/id/produk/jenis/shampo/3-in-1-clear-men-deep-cleanse-.html',
            '/id/perawatan-kulit-kepala/5-langkah-hilangkan-ketombe.html',
            '/id/perawatan-kulit-kepala/5-tips-keramas-tepat-dengan-shampo-anti-ketombe.html',
            '/id/home.html',
            '/id/produk/jenis/shampo/-clear-hijab-pure-shampo-anti-ketombe-&-anti-rontok.html',
            '/id/produk/jenis/shampo/clear-ice-cool-menthol-shampoo.html',
            '/id/produk/jenis/shampo/clear-lemon-anti-bacterial-shampoo.html',
            '/id/produk/jenis/shampo/clear-men-complete-care-shampoo.html',
            '/id/produk/jenis/shampo/clear-men-cool-sport-menthol-shampoo.html',
            '/id/perawatan-kulit-kepala/mitos-ketombe-terpecahkan.html',
            '/id/wanita.html',
            '/id/produk/jenis/shampo.html',
            '/id/pria.html',
        ],
        [
            '/vn/ren-luyen-tinh-than-dau-lanh-tim-nong/noi-dung-huong-dan-ren-luyen-dau-lanh-tim-nong.html',
            '/vn/cham-soc-da-dau/101-dieu-ve-cham-soc-da-dau-cho-ban-gai.html',
            '/vn/cham-soc-da-dau/5-buoc-de-loai-bo-gau.html',
            '/vn/cham-soc-da-dau/an-theo-cach-cua-ban-de-co-da-dau-va-mai-toc-khoe.html',
            '/vn/bai-viet-cho-nam-gioi.html',
            '/vn/bai-viet-cho-phu-nu.html',
            '/vn/cham-soc-da-dau/cach-dieu-tri-da-dau-kho.html',
            '/vn/cham-soc-da-dau.html',
            '/vn/gioi-thieu/chuyen-mon-cua-clear.html',
            '/vn/cham-soc-da-dau/da-dau-nhieu-dau-nguyen-nhan-va-cach-dieu-tri.html',
            '/vn/san-pham/loai/dau-goi.html',
            '/vn/cham-soc-da-dau/giai-phap-tri-gau-cho-moi-loai-da-dau.html',
            '/vn/cham-soc-da-dau/huong-dan-tri-gau-theo-phong-cach-dan-ong.html',
            '/vn/cham-soc-da-dau/khac-phuc-da-dau-ngua-ngay.html',
            '/vn/cham-soc-da-dau/lam-dịu-da-dau-ngua-ngay.html',
            '/vn/san-pham/loai/dau-goi/d u-g i-clear-men-cool-sport-b c-hà.html',
            '/vn/cham-soc-da-dau/nam-gioi-va-phu-nu-co-nen-su-dung-cung-mot-loai-dau-goi.html',
            '/vn/cham-soc-da-dau/nguyen-nhan-nao-gay-ra-gau.html',
            '/vn/cham-soc-da-dau/nhung-thuc-pham-tot-nhat-cho-toc-va-da-dau.html',
            '/vn/gioi-thieu/muc-dich-cua-chung-toi.html',
            '/vn/gioi-thieu/tu-tin-trong-xa-hoi.html',
            '/vn/cham-soc-da-dau/xua-tan-moi-loi-don-dai-ve-gau.html',
            '/vn/ren-luyen-tinh-than-dau-lanh-tim-nong/clear-purpose.html',
            '/vn/phu-nu.html',
            '/vn/san-pham/nhu-cau/lam-sach-sau.html',
            '/vn/cham-soc-da-dau/gau-la-gi.html',
            '/vn/bao-mat/Lien-he.html',
            '/vn/nam-gioi.html',
            '/vn/san-pham.html',
            '/vn/san-pham/loai/sua-tam.html',
            '/vn/san-pham/nhu-cau/chong-ngua.html',
            '/vn/san-pham/loai/dau-xa.html',
            '/vn/san-pham/loai/dau-goi/dầu-gội-clear-mát-lạnh-bạc-hà.html',
            '/vn/san-pham/loai/dau-goi/dầu-gội-clear-hoa-anh-đào.html',
            '/vn/san-pham/loai/dau-goi/dầu-gội-clear-men-cool-sport-bạc-hà.html',
            '/vn/san-pham/loai/dau-goi/dầu-gội-clear-men-deep-cleanse-sạch-sâu.html',
            '/vn/san-pham/loai/dau-goi/dầu-gội-clear-botanique-9-thảo-dược-quý.html',
            '/vn/dieu-khoan.html',
            '/vn/ren-luyen-tinh-than-dau-lanh-tim-nong/tai-sao-can-giu-vung-tinh-than-dau-lanh-tim-nong.html',
            '/vn/ren-luyen-tinh-than-dau-lanh-tim-nong/cach-ren-tinh-than-dau-lanh-tim-nong.html',
            '/vn/home.html',
        ],
        [
            '/br/about/clears-expertise.html',
            '/br/produtos/necessidades/alivio-da-coceira.html',
            '/br/produtos/necessidades/antioleosidade.html',
            '/br/produtos/tipo/condicionador.html',
            '/br/about/confianca-social.html',
            '/br/produtos/coleção/fusãoherbal.html',
            '/br/men.html',
            '/br/home.html',
            '/br/produtos/tipo/shampoo.html',
            '/br/produtos/necessidades/linha-sports.html',
            '/br/women.html',
            '/br/bora-jogar/bora-jogar-aulas.html',
            '/br/volte-mais-forte.html',
            '/br/produtos/tipo/condicionador/clear-conditioner-anti-dandruff-intense-hydration.html',
            '/br/produtos/tipo/condicionador/clear-conditioner-anti-dandruff-daily-detox.html',
            '/br/bora-jogar.html',
            '/br/about/eu-me-desafio-dos-pes-a-cabeca.html',
            '/br/about/nossa-visao.html',
            '/br/produtos/tipo/shampoo/clear-shampoo-anti-dandruff-intense-hydration.html',
            '/br/produtos/tipo/shampoo/clear-shampoo-anti-dandruff-detox-anti-pollution.html',
            '/br/produtos/tipo/shampoo/clear-shampoo-anti-dandruff-daily-detox.html',
            '/br/produtos/tipo/shampoo/clear-shampoo-anti-dandruff-sakura-flower.html',
            '/br/produtos/tipo/shampoo/clear-shampoo-anti-dandruff-itch-relief.html',
            '/br/produtos/tipo/shampoo/clear-shampoo-anti-dandruff-cool-sport.html',
            '/br/produtos/tipo/shampoo/clear-shampoo-anti-dandruff-hairfall-defense.html',
            '/br/produtos/tipo/shampoo/clear-shampoo-anti-dandruff-deep-clean0.html',
            '/br/produtos/tipo/shampoo/clear-shampoo-anti-dandruff-deep-clean.html',
        ],
        [
            '/th/scalp-care/5-steps-to-get-rid-of-dandruff.html',
            '/th/products/needs/anti-grease.html',
            '/th/products/type/shampoo.html',
            '/th/scalp-care.html',
            '/th/products/needs/anti-itch.html',
            '/th/products/type/conditioner.html',
            '/th/products.html',
            '/th/about/clears-expertise.html',
            '/th/men.html',
            '/th/scalp-care/should-men-and-women-use-the-same-shampoo.html',
            '/th/scalp-care/what-is-dandruff.html',
            '/th/scalp-care/soothe-your-itchy-scalp.html',
            '/th/scalp-care/the-dandruff-solution-for-every-scalp.html',
            '/th/scalp-care/how-to-treat-dry-scalp.html',
            '/th/about/our-purpose.html',
            '/th/women.html',
            '/th/scalp-care/oily-scalp-causes-and-treatments.html',
            '/th/home.html',
            '/th/scalp-care/what-causes-dandruff.html',
            '/th/products/type/shampoo/เมน-แอนตี้แฮร์ฟอล-แอนตี้แดนดรัฟ-แชมพู-.html',
            '/th/products/type/shampoo/เมน-คูลสปอร์ต-เมนทอล-แอนตี้แดนดรัฟ-แชมพู-.html',
            '/th/products/type/shampoo/เมน-ดีพคลีนส์-แอนตี้แดนดรัฟ-แชมพู-.html',
            '/th/products/type/shampoo/เฮอร์บัลแคร์-แอนตี้แดนดรัฟ-สกาล์ปแคร์-แชมพู-.html',
            '/th/products/type/shampoo/แอนตี้แฮร์ฟอล-แอนตี้แดนดรัฟ-สกัลป์แคร์-แชมพู-.html',
            '/th/products/type/shampoo/โบทานีค-นอริช-แอนด์-เฮลธี-สกาล์ปแคร์-แชมพู.html',
            '/th/products/type/shampoo/โบทานีค-บาลานซ์-แอนด์-เบาวน์ซี่-สกาล์ปแคร์-แชมพู.html',
            '/th/products/type/shampoo/ไอซ์คูล-เมนทอล-แอนตี้แดนดรัฟ-สกาล์ปแคร์-แชมพู-.html',
            '/th/products/type/shampoo/แชมพู-ซากุระเฟรช-แอนตี้แดนดรัฟ-สกาล์ปแคร์-.html',
            '/th/products/type/shampoo/ยูซุ-&-มิ้นท์-แอนตี้แดนดรัฟ-สกาล์ปแคร์-แชมพู.html',
            '/th/products/type/shampoo/เคลียร์-สกาล์ปเทอราพี-เพียวริฟายอิ้ง-ไมเซล่า-แอนตี้แดนดรัฟ-แชมพู.html',
            '/th/products/type/shampoo/เคลียร์-สกาล์ปเทอราพี-ไฮเดรติ้ง-ไมเซล่า-แอนตี้แดนดรัฟ-แชมพู.html',
        ],
        [
            '/tr/goster-kendini/bacak-boyu-uzatma.html',
            '/tr/goster-kendini/bacak-inceltme-hareketleri.html',
            '/tr/goster-kendini/basen-eritme.html',
            '/tr/goster-kendini/biceps-hareketleri.html',
            '/tr/goster-kendini/bilek-guclendirme.html',
            '/tr/goster-kendini/farkli-hizli-kosma-teknikleri.html',
            '/tr/goster-kendini/bisiklet-surmek-kaslar.html',
            '/tr/urunler/tur/sampuan/bitkisel-sentez-kadin-sampuan.html',
            '/tr/guvenli/bize-ulasin.html',
            '/tr/goster-kendini/boy-uzatma-egzersizleri.html',
            '/tr/goster-kendini/bulk-nedir.html',
            '/tr/ronaldo.html',
            '/tr/urunler/tur/sampuan.html',
            '/tr/hakkimizda/clear-uzmanligi.html',
            '/tr/urunler/tur/sampuan/cool-sport-menthol-erkek-sampuan.html',
            '/tr/urunler/tur/sampuan/men-cool-sport-menthol.html',
            '/tr/goster-kendini/daha-siki-bir-vucut-icin-egzersizler.html',
            '/tr/goster-kendini/dambil-egzersizleri.html',
            '/tr/goster-kendini/definasyon-nedir.html',
            '/tr/goster-kendini/etkili-bacak-egzersizleri.html',
            '/tr/urunler/tur/sampuan/dus-ferahligi-erkek-sampuan.html',
            '/tr/sac-derisi-bakimi/sasirtici-erkek-sac-derisi-sirlari.html',
            '/tr/erkek-sac-derisi-bakimi.html',
            '/tr/goster-kendini/sac-modelleri-isimleri.html',
            '/tr/erkek.html',
            '/tr/sac-derisi-bakimi/erkekler-kadinlar-sampuan-secimi.html',
            '/tr/sac-derisi-bakimi/kepekten-kurtulma-rehberi.html',
            '/tr/goster-kendini/evde-fitness.html',
            '/tr/goster-kendini/evde-kolay-egzersiz.html',
            '/tr/fitness-makaleler/sporcu-beslenmesi.html',
            '/tr/goster-kendini/gobek-eritme.html',
            '/tr/goster-kendini/haftada-kac-gun-spor.html',
            '/tr/sac-derisi-bakimi/kadin-sac-derisi-bakimina-giris.html',
            '/tr/goster-kendini/hizli-kilo-verme.html',
            '/tr/urunler/tur/sampuan/men-ikisibirarada.html',
            "/tr/urunler/tur/sampuan/hizli-stil-2'si - 1 - arada - erkek - sampuan.html",
            '/tr/goster-kendini/fitness-terimleri.html',
            '/tr/goster-kendini/ideal-kilo-hesaplama.html',
            '/tr/goster-kendini/ip-atlamanin-faydalari.html',
            '/tr/kadin.html',
            '/tr/sac-derisi-bakimi/kadinlar-icin-sac-derisi-bakimi.html',
            '/tr/goster-kendini/karin-kasi-hareketleri.html',
            '/tr/home.html',
            '/tr/sac-derisi-bakimi/tum-sac-derileri-icin-kepek-cozumleri.html',
            '/tr/sac-derisi-bakimi/kepekten-kurtulmanin-adimlari.html',
            '/tr/sac-derisi-bakimi/kepek-nedir.html',
            '/tr/goster-kendini/kilo-alma-diyeti.html',
            '/tr/goster-kendini/kilo-almaya-yardimci-gidalar.html',
            '/tr/urunler/tur/sampuan/komple-bakim-kadin-sampuan.html',
            '/tr/goster-kendini/kosu-oncesi-isinma.html',
            '/tr/urunler/ihtiyaclar/onarim.html',
            '/tr/legend-by-cr7.html',
            '/tr/goster-kendini/masa-tenisi-nasil-oynanir.html',
            '/tr/goster-kendini/omuz-genisletme-hareketleri.html',
            '/tr/goster-kendini/posturunuzu-duzeltecek-sirt-kaslari-hareketleri.html',
            '/tr/sac-derisi-bakimi/kasintili-sac-derisinden-kurtul.html',
            '/tr/urunler/tur/sampuan/sac-dokulmesine-karsi-etkin-savunma-erkek-sampuan.html',
            '/tr/urunler/tur/sampuan/sac-dokulmesine-karsi-kadin-sampuan.html',
            '/tr/urunler.html',
            '/tr/sikca-sorulan-sorular.html',
            '/tr/goster-kendini/sinav-cekme.html',
            '/tr/goster-kendini/isinma-hareketleri.html',
            '/tr/goster-kendini/hamlik-agrisi-nasil-gecer.html',
            '/tr/goster-kendini/spordan-once-ne-yemeli.html',
            '/tr/goster-kendini/tenis-nasil-oynanir.html',
            '/tr/goster-kendini/fitness-programi.html',
            '/tr/goster-kendini/vucut-tipleri.html',
            '/tr/goster-kendini/vucut-yag-orani-hesaplama.html',
            '/tr/urunler/tur/sampuan/yagli-sac-derisi-icin-erkek-sampuan.html',
            '/tr/urunler/tur/sampuan/yagli-sac-derisi-icin-etkin-kontrol-kadin-sampuan.html',
            '/tr/urunler/ihtiyaclar/yagli-saclar-icin.html',
            '/tr/urunler/tur/sampuan/yumusak-parlak-kiraz-cicegi-kadin-sampuan.html',
            '/tr/goster-kendini/erkek-yuz-sekline-gore-sac.html',
            '/tr/goster-kendini/yuzme-teknikleri.html',
        ],
        [
            '/ru/scalp-care/5-steps-to-get-rid-of-dandruff.html',
            '/ru/home.html',
            '/ru/products/type/conditioner.html',
            '/ru/about/our-purpose.html',
            '/ru/articles-for-women.html',
            '/ru/scalp-care.html',
            '/ru/products/type/shampoo.html',
            '/ru/about/clears-expertise.html',
            '/ru/products/type/conditioner/clear-intense-hydration-conditioner.html',
            '/ru/products.html',
            '/ru/scalp-care/oily-scalp-causes-and-treatments.html',
            '/ru/scalp-care/greasy-hair.html',
            '/ru/scalp-care/kak-vyglyadyat-zdorovyye-volosy.html',
            '/ru/scalp-care/kak-izbavitsya-ot-perkhoti-bystro-i-effektivno.html',
            '/ru/scalp-care/kak-ostanovit-vypadeniye-volos.html',
            '/ru/scalp-care/kak-sdelat-volosy-blestyashchimi.html',
            '/ru/scalp-care/kak-spravitsya-s-zudom-kozhi-golovi.html',
            '/ru/scalp-care/how-to-treat-dry-scalp.html',
            '/ru/women.html',
            '/ru/men.html',
            '/ru/scalp-care/dandruff-myths-busted.html',
            '/ru/products/type/conditioner/clear-color-damaged-conditioner.html',
            '/ru/scalp-care/kak-isportit-volosy.html',
            '/ru/faq.html',
            '/ru/scalp-care/Pakhnet-kozha-golovy-Chto-delat.html',
            '/ru/secure/contactus.html',
            '/ru/scalp-care/pochemu-volosy-stanovyatsya-sukhimi.html',
            '/ru/scalp-care/soothe-your-itchy-scalp.html',
            '/ru/scalp-care/end-itchy-scalp-for-good.html',
            '/ru/scalp-care/the-mens-guide-to-busting-dandruff-in-style.html',
            '/ru/scalp-care/tips-from-clear-how-to-wash-your-hair-with-shampoo.html',
            '/ru/about/come-back-stronger-clear.html',
            '/ru/scalp-care/Tipy-kozhi-golovy-Kak-opredelit-tip-kozhi-golovy.html',
            '/ru/scalp-care/pravila-uhoda-za-volosami-posle-keratinovogo-vypryamleniya.html',
            '/ru/scalp-care/chem-otlichaetsya-muzhskoy-shampun-ot-zhenskogo.html',
            '/ru/scalp-care/what-causes-dandruff.html',
            '/ru/scalp-care/what-is-dandruff.html',
            '/ru/products/type/shampoo/clear-oil-control-balance-shampoo.html',
            '/ru/products/type/shampoo/clear-color-damaged-shampoo.html',
            '/ru/products/type/shampoo/clear-men-phytotechnology-shampoo.html',
            '/ru/products/type/shampoo/clear-anti-hairfall-shampoo.html',
            '/ru/products/type/shampoo/clear-ultimate-control-2in1-shampoo.html',
            '/ru/products/type/shampoo/clear-shampoo-and-conditioner-2in-1-activesport.html',
            '/ru/products/type/shampoo/clear-shampoo-and-conditioner-2in-1-deep-clense.html',
            '/ru/products/type/shampoo/clear-intense-hydration-shampoo.html',
            '/ru/products/type/shampoo/clear-men-ice-fresh-shampoo.html',
            '/ru/products/type/shampoo/clear-volume-maxx-shampoo.html',
            '/ru/products/type/shampoo/clear-complete-care-shampoo.html',
            '/ru/products/type/shampoo/clear-phytotechnology-shampoo.html',
            '/ru/products/type/shampoo/clear-men-anti-hairfall-shampoo.html',
            '/ru/products/type/shampoo/clear-men-shower-fresh-shampoo.html',
        ]
    ]

    page_ids = [
        'a116178497w103157272p107273512', #ID
        'a116178497w86333592p89585249', #VN
        'a116178497w207606669p200288299', #BR
        'a116178497w86386756p89631753', #TH
        'a116178497w97233771p101371256', #TR
        'a116178497w86398311p89642028', #RU
    ]

    return urls, page_ids


def get_data2(urls, page_id):

    global sheet_p, sheet_n

    start_date = '20200701'
    end_date = '20200930'

    base_url = 'https://analytics.google.com/analytics/web/getPage?_u.date00=' + start_date + '&_u.date01=' + end_date + \
               '&_r.tabId=navigationsummary&id=content-pages&ds=' + page_id + '&cid=navigationsummary%2CreportHeader%2CtabControl%2CtimestampMessage&hl=en_GB&authuser=1&sstPremiumUser=true'
    body = {
        'token': x_token,
    }

    reg = 'rowCluster":(.*?)"clusteredRowLabel'
    detail_reg = '"displayKey":"(.*?)".*?dataValue":"(.*?)".*?dataValue":"(.*?)"'

    for url in urls:
        try:
            target_url = base_url + '&_r.drilldown=analytics.pagePath:' + url.replace('/', '%2f')
            print target_url
            html = post_request_html(target_url, cookie, data=body)
            raw = re.compile(reg).findall(html)

            if raw:
                datas = re.compile(detail_reg).findall(raw[0])
                for data in datas:
                    one_row = [url, data[0], data[1], data[2]]
                    print one_row
                    sheet_p.append(one_row)
                datas = re.compile(detail_reg).findall(raw[1])
                for data in datas:
                    one_row = [url, data[0], data[1], data[2]]
                    print one_row
                    sheet_n.append(one_row)
        except Exception as e:
            print 'err--', url, e


def get_sheet3():
    urls = prepare_url()
    head = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'origin': 'https://analytics.google.com',
        'referer': 'https://analytics.google.com/analytics/app/?authuser=1',
        'x-client-data': 'CLG1yQEIh7bJAQimtskBCMG2yQEIqZ3KAQioo8oBCLGnygEI4qjKAQjxqcoBCMuuygEI97TKAQ==',
    }

    target_url = 'https://analytics.google.com/analytics/web/exportReport?hl=en_GB&authuser=1&sstPremiumUser=true&ef=XLSX'

    for url in urls[1:]:
        body = {
            '_u.date00': '20190901',
            '_u.date01': '20191201',
            'search_console-table.plotKeys': '[]',
            'search_console-table.rowStart': '0',
            'search_console-table.rowCount': '5000',
            '_r.drilldown': 'analytics.landingPagePath:' + url,
            'id': 'acquisition-sc-landingpages',
            'ds': 'a116178497w103157272p107273512',
            'exportUrl': 'https://analytics.google.com/analytics/web/?authuser=1#/report/acquisition-sc-landingpages/a116178497w103157272p107273512/_u.date00=20190901&_u.date01=20191201&search_console-table.plotKeys=%5B%5D&search_console-table.rowStart=0&search_console-table.rowCount=5000&_r.drilldown=analytics.landingPagePath:' + url.replace('/', '~2F'),
        }

        try:
            get_attachments(target_url, url.replace('/', '_') + '.xlsx', headers=head, data=body)
        except Exception as e:
            print 'err-', target_url, e


urls, page_ids = prepare_url()

for i in range(len(urls)):
    get_data2(urls[i], page_ids[i])
write_excel('data/previous.xls', sheet_p)
write_excel('data/next.xls', sheet_n)