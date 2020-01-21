from scraping import utils
import re
import urllib
import xlrd
import time

sheet1 = [['UID', 'Product Name', 'url', 'Rating', 'No. of Ratings', 'Questions unanswered']]
sheet2 = [['UID', 'url', 'question', 'votes']]
sheet3 = [['UID', 'url', 'Review Mentions']]

cookie1 = 'csm-sid=751-4089195-0673484; x-amz-captcha-1=1575482102774162; x-amz-captcha-2=kOElJgc+qIBAOf7EcSh8mw==; session-id=137-3119642-8558756; session-id-time=2082787201l; sp-cdn="L5Z9:SG"; ubid-main=134-3149591-2048805; x-wl-uid=1jZ7Ci7dAHogJljIb1+/lCw08BUB0fBZkmVRgcuqDJxUhhGfkmTZGqMDzSuRs9TEKESAy+CbZ9Cg=; lc-main=en_US; csm-hit=tb:K0PM1TV1R6GGD1PCE8P6+s-R1YS5R1RA5CPRFXKS56Z|1575482628934&t:1575482628934&adb:adblk_yes; a-ogbcbff=1; session-token="ltytRLpEKXtJ85M95MClq/JuGkTauMyMzpLqXjCUXOQaBozlX+yuRnhvOvmFkvZBdS+gUxqRcNUGOssa4id/+6vylKOlZSBPboJRvksC5mhfKXMp3e9M2GhqCRT1xEFKm6VBvJlAxN+NEl8plF7I2L6v3+HsresdBCNoUqSxZXMY4z9hGr1J9oftOkzRF+JQ3AuBjAPqamBHNVWyvzEBTy7YUZU+tAqA/FjMi3yGXug="; x-main="AwPc2nnLHwljIHLRedrh6EV6Ys8EG4e?4QQRFChU8L@52Cs2z6QXc5jMKzsM3dUJ"; at-main=Atza|IwEBIFjbprrkk_xoTcUneyuNpT0HP5IXeyYaA_n_M-S8cddoV_jE80mQyhYY3z6X0hezZit6hEQfID79BCP3IPTPDFFRDIyFZnPcsfX_yCzq7ogng-RVKOS8Dwy7RahJ0APYJIzZwUB8Av7Hs-2Qv_hxG9jCqZqEZrb2nCWIZWz4Z6zHzwMdx669w9LRjs51LOM_Xu3Y5naLZ3RsxogFKhrcuuOPJcYiD3WGGiSfp964eabFiQj4vxLlQYRiKkDfisfdpbB9gjP5yqSgLF8YkJu0bzBEc0UwXa9sSwAjHy7gxeRKn9XMjncEAyTmPfvNl-zeU5023_UUXemddKRYIeFomnXfqB3r2x_OQqYGgl8iZ4qC0COxqHo6dGVi8LOJ7pEtiLcuZ8F8ZsKD_ABB8MRtKWUObeSqkN7VtJw7IYP5BPL1pzpcO7HvGZ-yIkSOiStiXd0; sess-at-main="hrNQDZU2/m360P2eEbywpzCCeSOMX68NUK0nR1LG190="; sst-main=Sst1|PQFDHngnNP6a-61SmZ7cFI45C9TX9JfR8nAYtMr46JtZFnMPTxm4DzuAIIodjeOMVPzGXhuMIlvcJMVQ61ujp7TdkpboDg3d_53VfFAlYxbeM-b1nhA84Vv1CPZE-XpS1g3Aj7OFdAP06lmUI1l9OhN052f7Vt-cxZvdQzEyCx04NKKDkLxg8UubsjdrLslidi2fKAQpGCBuPrPwgDETEphhKOAg4XXyhSqKaPjBR53zsg6hfkUfOhOri-vrmRPbQ98EwJcyAE1beUwawAHrCL-BOI1tIIMiAoZWza8FjXRDKSU4KxTO3pKNV6tyCGm0yHIbfAqf9cycJQmD2oGfbj6YUA'
cookie2 = 'csm-sid=751-4089195-0673484; x-amz-captcha-1=1575482102774162; x-amz-captcha-2=kOElJgc+qIBAOf7EcSh8mw==; session-id=137-3119642-8558756; session-id-time=2082787201l; sp-cdn="L5Z9:SG"; ubid-main=134-3149591-2048805; x-wl-uid=1jZ7Ci7dAHogJljIb1+/lCw08BUB0fBZkmVRgcuqDJxUhhGfkmTZGqMDzSuRs9TEKESAy+CbZ9Cg=; lc-main=en_US; i18n-prefs=USD; csm-hit=tb:s-V35D0YF1QZ847QPD34ZT|1575481041570&t:1575481043206&adb:adblk_yes; session-token=j6tNEXvw48DkBv+tLyGlN+o8QLehj50x1CkBpUTr0kT5+7LttG/ZyYBEeOTX5hlK1os7eBTMNsQXpfvLTZ40OBXyOvLb6XJcEQNYrZ1FQNRMVpsgJRfKcTHD5XnIoHfn1Z4vjntFSxx4Ms3nsUO9B8N7AG2jYfQkjffwFOO5j+4XuAzoScDUMDvK5yKTbOSy'
G_ID = 1

urls = [
    # 'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_aps_sr_pg1_1?ie=UTF8&amp;adId=A08086394RCURB1HKEGY&amp;url=%2FGenuine-Xerox-Capacity-Cartridge-106R04347%2Fdp%2FB07VV6QS5M%2Fref%3Dsr_1_1_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550205%26sr%3D8-1-spons%26psc%3D1&amp;qualifier=1575550205&amp;id=935455718439893&amp;widgetName=sp_atf',
    # 'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_aps_sr_pg1_2?ie=UTF8&amp;adId=A03767223BY5XRPXNVAS9&amp;url=%2FGenuine-Xerox-Cartridge-WorkCentre-106R02243%2Fdp%2FB0098NP0VY%2Fref%3Dsr_1_2_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550205%26sr%3D8-2-spons%26psc%3D1&amp;qualifier=1575550205&amp;id=935455718439893&amp;widgetName=sp_atf',
    # 'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_aps_sr_pg1_3?ie=UTF8&amp;adId=A07151871ZBOTHWL3TT6G&amp;url=%2FBAISINE-Compatible-Cartridge-Laserjet-Printer%2Fdp%2FB07YZ5VGS9%2Fref%3Dsr_1_3_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550205%26sr%3D8-3-spons%26psc%3D1&amp;qualifier=1575550205&amp;id=935455718439893&amp;widgetName=sp_atf',
    # 'https://www.amazon.com/Brother-Genuine-TN660-Yield-Cartridge/dp/B00LJO8EQS/ref=sxin_3_ac_d_rm?ac_md=0-0-cHJpbnRlciB0b25lcg%3D%3D-ac_d_rm&amp;keywords=printer+toner&amp;pd_rd_i=B00LJO8EQS&amp;pd_rd_r=c984d710-a004-4004-b31c-866948931b68&amp;pd_rd_w=4Zg7Q&amp;pd_rd_wg=7iB3Q&amp;pf_rd_p=6d29ef56-fc35-411a-8a8e-7114f01518f7&amp;pf_rd_r=6W6YTVKXTK4C2NPJRC9Y&amp;psc=1&amp;qid=1575550205',
    # 'https://www.amazon.com/Brother-HL-L2300D-Monochrome-Printer-Printing/dp/B00NQ1CLTI/ref=sxin_3_ac_d_rm?ac_md=1-1-cHJpbnRlciBsYXNlcg%3D%3D-ac_d_rm&amp;keywords=printer+toner&amp;pd_rd_i=B00NQ1CLTI&amp;pd_rd_r=c984d710-a004-4004-b31c-866948931b68&amp;pd_rd_w=4Zg7Q&amp;pd_rd_wg=7iB3Q&amp;pf_rd_p=6d29ef56-fc35-411a-8a8e-7114f01518f7&amp;pf_rd_r=6W6YTVKXTK4C2NPJRC9Y&amp;psc=1&amp;qid=1575550205&amp;smid=ATVPDKIKX0DER',
    'https://www.amazon.com/Brother-Genuine-Cartridge-TN450-Replacement/dp/B003YFHCKY/ref=sxin_3_ac_d_rm?ac_md=2-2-dG40NTA%3D-ac_d_rm&amp;keywords=printer+toner&amp;pd_rd_i=B003YFHCKY&amp;pd_rd_r=c984d710-a004-4004-b31c-866948931b68&amp;pd_rd_w=4Zg7Q&amp;pd_rd_wg=7iB3Q&amp;pf_rd_p=6d29ef56-fc35-411a-8a8e-7114f01518f7&amp;pf_rd_r=6W6YTVKXTK4C2NPJRC9Y&amp;psc=1&amp;qid=1575550205',
    'https://www.amazon.com/HP-Tri-color-Original-Cartridges-F6U61AN/dp/B00WR23VRI/ref=sxin_3_ac_d_rm?ac_md=3-3-cHJpbnRlciBpbms%3D-ac_d_rm&amp;keywords=printer+toner&amp;pd_rd_i=B00WR23VRI&amp;pd_rd_r=c984d710-a004-4004-b31c-866948931b68&amp;pd_rd_w=4Zg7Q&amp;pd_rd_wg=7iB3Q&amp;pf_rd_p=6d29ef56-fc35-411a-8a8e-7114f01518f7&amp;pf_rd_r=6W6YTVKXTK4C2NPJRC9Y&amp;psc=1&amp;qid=1575550205',
    'https://www.amazon.com/Brother-Genuine-TN660-Yield-Cartridge/dp/B00LJO8EQS/ref=sr_1_4?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-4',
    'https://www.amazon.com/Brother-DCP-L2550DW-HL-L2350DW-MFC-L2710-Replacement/dp/B075X6C5ZW/ref=sr_1_5?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-5',
    'https://www.amazon.com/HP-Cartridge-Magenta-Cartridges-LaserJet/dp/B01NB0P9K5/ref=sr_1_6?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-6',
    'https://www.amazon.com/Brother-Genuine-Cartridge-TN450-Replacement/dp/B003YFHCKY/ref=sr_1_7?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-7',
    'https://www.amazon.com/Brother-Monochrome-Multifunction-MFCL2710DW-Replenishment/dp/B0763ZCH7K/ref=sr_1_8?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-8',
    'https://www.amazon.com/HP-Cartridge-Magenta-Cartridges-LaserJet/dp/B01MQXPZ5R/ref=sr_1_9?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-9',
    'https://www.amazon.com/Brother-DCP-L5500-HL-L5000D-Cartridge-Packaging/dp/B01825OGPE/ref=sr_1_10?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-10',
    'https://www.amazon.com/GPC-Image-Compatible-Cartridge-Replacement/dp/B07RXJ9B4M/ref=sr_1_11?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-11',
    'https://www.amazon.com/Toner-CF410A-CF411A-CF412A-CF413A/dp/B07KY5NZ1G/ref=sr_1_12?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-12',
    'https://www.amazon.com/Brother-Genuine-Cartridge-TN420-Replacement/dp/B003YFHCK4/ref=sr_1_13?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-13',
    'https://www.amazon.com/HP-CF226A-Black-Cartridge-LaserJet/dp/B015H31W60/ref=sr_1_14?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-14',
    'https://www.amazon.com/Brother-Cartridge-TN630-Replacement-Replenishment/dp/B00LGCUPQU/ref=sr_1_15?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-15',
    'https://www.amazon.com/Brother-TN730-DCP-L2550DW-MFC-L2710DW-MFC-L2750DW/dp/B075X7TFY5/ref=sr_1_16?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-16',
    'https://www.amazon.com/Canon-imageCLASS-LBP6230dw-Wireless-Printer/dp/B00MWDUXZ0/ref=sr_1_17?keywords=printer+toner&amp;qid=1575550205&amp;smid=ATVPDKIKX0DER&amp;sr=8-17',
    'https://www.amazon.com/LINKYO-Compatible-Cartridge-Replacement-Brother/dp/B00S0BENC2/ref=sr_1_18?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-18',
    'https://www.amazon.com/HP-MLT-D111S-Cartridge-SL-M2020W-SU814A/dp/B00IQBT1AK/ref=sr_1_19?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-19',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg1_1?ie=UTF8&amp;adId=A0105624W7B9S5R6LPJ0&amp;url=%2FFourFahrenheit-Repackaged-Unused-Original-Cartridges%2Fdp%2FB07W9FC9ZF%2Fref%3Dsr_1_20_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550205%26sr%3D8-20-spons%26psc%3D1&amp;qualifier=1575550205&amp;id=935455718439893&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg1_2?ie=UTF8&amp;adId=A0902456S2SAIFGNQGXL&amp;url=%2FSINOPRINT-Compatible-E260A11A-Lexmark-E460dtn%2Fdp%2FB081S3PPS2%2Fref%3Dsr_1_21_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550205%26sr%3D8-21-spons%26psc%3D1&amp;qualifier=1575550205&amp;id=935455718439893&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg1_3?ie=UTF8&amp;adId=A06515301HXNB1UKA47CG&amp;url=%2FCompatible-CRG-051-Toner-Cartridge-Replacements%2Fdp%2FB07C4SWWTP%2Fref%3Dsr_1_22_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550205%26sr%3D8-22-spons%26psc%3D1&amp;qualifier=1575550205&amp;id=935455718439893&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg1_4?ie=UTF8&amp;adId=A048930320O0Q8S0S343J&amp;url=%2FmyCartridge-Compatible-Cartridge-Replacement-Laserjet%2Fdp%2FB07VNLLF7F%2Fref%3Dsr_1_23_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550205%26sr%3D8-23-spons%26psc%3D1&amp;qualifier=1575550205&amp;id=935455718439893&amp;widgetName=sp_mtf',
    'https://www.amazon.com/HP-Laserjet-Monochrome-Two-Sided-4PA41A/dp/B07HB18C2V/ref=sr_1_24?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-24',
    'https://www.amazon.com/Brother-Monochrome-Multifunction-DCPL2550DW-Replenishment/dp/B0764P8F5J/ref=sr_1_25?keywords=printer+toner&amp;qid=1575550205&amp;smid=ATVPDKIKX0DER&amp;sr=8-25',
    'https://www.amazon.com/Ink-TN760-TN-760-TN730-TN-730/dp/B07L63868D/ref=sr_1_26?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-26',
    'https://www.amazon.com/HP-CF410A-Cartridge-Laserjet-M477fdn/dp/B0156KUB5M/ref=sr_1_27?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-27',
    'https://www.amazon.com/HP-CF226X-Original-Cartridge-Laserjet/dp/B015H31XZ0/ref=sr_1_28?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-28',
    'https://www.amazon.com/Brother-Genuine-TN221C-Magenta-Cartridge/dp/B0141MWYCY/ref=sr_1_29?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-29',
    'https://www.amazon.com/Brother-TN630-Standard-Cartridge-Approximately/dp/B07QC959FC/ref=sr_1_30?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-30',
    'https://www.amazon.com/Cool-Toner-Compatible-Cartridge-Replacement/dp/B07H8TSRH8/ref=sr_1_31?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-31',
    'https://www.amazon.com/GPC-Image-5-Pack-Compatible-Replacement/dp/B07DFKL53V/ref=sr_1_32?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-32',
    'https://www.amazon.com/Ink-Replacement-MFC-L2700DW-MFC-L2720DW-MFC-L2740DW/dp/B00NY6QUP6/ref=sr_1_33?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-33',
    'https://www.amazon.com/Dougs-Story/dp/B01NH2WRZK/ref=sr_1_34?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-34',
    'https://www.amazon.com/Brother-Monochrome-HL-L2350DW-Two-Sided-Replenishment/dp/B0763WDSYZ/ref=sr_1_35?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-35',
    'https://www.amazon.com/Brother-TN221BK-TN-221BK-Complete-Cartridge/dp/B00V2LTU2A/ref=sr_1_36?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-36',
    'https://www.amazon.com/IKONG-Replacement-DCP-L2540DW-DCP-L2520DW-MFC-L2700DW/dp/B06XDDSY88/ref=sr_1_37?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-37',
    'https://www.amazon.com/Canon-Original-120-Toner-Cartridge/dp/B001TOD3NM/ref=sr_1_38?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-38',
    'https://www.amazon.com/GREENSKY-TN630-MFC-L2700DW-DCP-L2540DW-MFC-L2720DW/dp/B014S6NZR6/ref=sr_1_39?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-39',
    'https://www.amazon.com/Brother-Reseller-TN-660-Cartridge-2-Pack/dp/B078HJFGF9/ref=sr_1_40?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-40',
    'https://www.amazon.com/LINKYO-Compatible-Cartridge-Replacement-Brother/dp/B07DRTLLNC/ref=sr_1_41?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-41',
    'https://www.amazon.com/HP-CF500X-Original-Cartridge-LaserJet/dp/B074KRP89L/ref=sr_1_42?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-42',
    'https://www.amazon.com/HP-CF500A-Original-Cartridge-LaserJet/dp/B074KTXVYP/ref=sr_1_43?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-43',
    'https://www.amazon.com/Replacement-202X-CF500A-CF500X-202A/dp/B07MCBRXP8/ref=sr_1_44?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-44',
    'https://www.amazon.com/Canon-Original-137-Toner-Cartridge/dp/B00N99DC8Q/ref=sr_1_45?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-45',
    'https://www.amazon.com/Brother-Cartridge-TN221BK-Replacement-Replenishment/dp/B00BR3WWY6/ref=sr_1_46?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-46',
    'https://www.amazon.com/Ink-Replacement-DCP-L2520DW-DCP-L2540DW-MFC-L2707DW/dp/B00NY6WB9K/ref=sr_1_47?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-47',
    'https://www.amazon.com/HP-CF248A-Black-Cartridge-Laserjet/dp/B07B6LKF98/ref=sr_1_48?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-48',
    'https://www.amazon.com/Ink-Replacement-MFC-L2700DW-MFC-L2720DW-MFC-L2740DW/dp/B07G131Z6Y/ref=sr_1_49?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-49',
    'https://www.amazon.com/HP-CF341A-Original-LaserJet-Cartridges/dp/B007B5SMF2/ref=sr_1_50?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-50',
    'https://www.amazon.com/HP-CF280A-Black-Cartridge-LaserJet/dp/B007RHU144/ref=sr_1_51?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-51',
    'https://www.amazon.com/Ink-Replacement-MFC-L2700DW-MFC-L2720DW-MFC-L2740DW/dp/B00NY6OLCK/ref=sr_1_52?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-52',
    'https://www.amazon.com/Brother-TN660-cartridge-retail-packaging/dp/B00QKVIH5S/ref=sr_1_53?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-53',
    'https://www.amazon.com/HP-CF410X-Cartridge-LaserJet-M477fdn/dp/B0156KULRA/ref=sr_1_54?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-54',
    'https://www.amazon.com/Canon-Original-128-Toner-Cartridge/dp/B0041RRMQS/ref=sr_1_55?keywords=printer+toner&amp;qid=1575550205&amp;sr=8-55',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg1_1?ie=UTF8&amp;adId=A0814249NH8U97IJAK3T&amp;url=%2FBAISINE-Compatible-Cartridge-Replacement-Laserjet%2Fdp%2FB07XBRKYF7%2Fref%3Dsr_1_56_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550205%26sr%3D8-56-spons%26psc%3D1&amp;qualifier=1575550205&amp;id=935455718439893&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg1_2?ie=UTF8&amp;adId=A02604411PAOLRYT9MM71&amp;url=%2FmyCartridge-Re-Manufactured-Cartridge-Replacement-Magenta%2Fdp%2FB07STV89PP%2Fref%3Dsr_1_57_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550205%26sr%3D8-57-spons%26psc%3D1&amp;qualifier=1575550205&amp;id=935455718439893&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg1_3?ie=UTF8&amp;adId=A05498501XEJBX8EM3FOJ&amp;url=%2FOCProducts-Refilled-Cartridge-Replacement-Officejet%2Fdp%2FB072FNFCMH%2Fref%3Dsr_1_58_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550205%26sr%3D8-58-spons%26psc%3D1&amp;qualifier=1575550205&amp;id=935455718439893&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg1_4?ie=UTF8&amp;adId=A08593562JH3QYO1YHR1Z&amp;url=%2FAutomatic-Cartridge-MFC-7860DW-DCP-7065DN-Intellifax%2Fdp%2FB07V6R3PGV%2Fref%3Dsr_1_59_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550205%26sr%3D8-59-spons%26psc%3D1&amp;qualifier=1575550205&amp;id=935455718439893&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg1_5?ie=UTF8&amp;adId=A09555111F0KIY6PB8R94&amp;url=%2FCMCMCM-Compatible-Cartridge-Replacement-Laserjet%2Fdp%2FB07XXMDX4Y%2Fref%3Dsr_1_60_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550205%26sr%3D8-60-spons%26psc%3D1&amp;qualifier=1575550205&amp;id=935455718439893&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg2_1?ie=UTF8&amp;adId=A03688103CUEHC7XGYECR&amp;url=%2FGenuine-Xerox-Cartridge-WorkCentre-106R02241%2Fdp%2FB0098NP01Y%2Fref%3Dsr_1_49_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550207%26sr%3D8-49-spons%26psc%3D1&amp;qualifier=1575550206&amp;id=420249696206537&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg2_2?ie=UTF8&amp;adId=A00492265CFGJJBFWXW9&amp;url=%2FLexmark-MC3224adwe-Multifunction-Capabilities-Full-Spectrum%2Fdp%2FB07T4LGDGQ%2Fref%3Dsr_1_50_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550207%26sr%3D8-50-spons%26psc%3D1&amp;qualifier=1575550206&amp;id=420249696206537&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg2_3?ie=UTF8&amp;adId=A0838785243V5NSS0620E&amp;url=%2FSotek-Compatible-Cartridge-Replacement-934XL%2Fdp%2FB07H32PW5N%2Fref%3Dsr_1_51_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550207%26sr%3D8-51-spons%26psc%3D1&amp;qualifier=1575550206&amp;id=420249696206537&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg2_4?ie=UTF8&amp;adId=A0481814SA599QFY0XZP&amp;url=%2FINSMAX-Remanufactured-Replacement-TS302Printer-1Tri-Color%2Fdp%2FB07GFJK16M%2Fref%3Dsr_1_52_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550207%26sr%3D8-52-spons%26psc%3D1&amp;qualifier=1575550206&amp;id=420249696206537&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/HP-CF400A-Cartridge-Laserjet-M252dw/dp/B00UBMNYM8/ref=sr_1_53?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-53',
    'https://www.amazon.com/Canon-Cartridge-3009C001-imageCLASS-LBP228dw/dp/B07WWK22KW/ref=sr_1_54?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-54',
    'https://www.amazon.com/Brother-Monochrome-HLL2395DW-Cloud-Based-Replenishment/dp/B0764NWFP8/ref=sr_1_55?keywords=printer+toner&amp;qid=1575550207&amp;smid=ATVPDKIKX0DER&amp;sr=8-55',
    'https://www.amazon.com/HP-CF217A-Original-Cartridge-Laserjet/dp/B01LBWEL1E/ref=sr_1_56?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-56',
    'https://www.amazon.com/Brother-Genuine-Cartridge-Replacement-Replenishment/dp/B07FNKJD24/ref=sr_1_57?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-57',
    'https://www.amazon.com/HP-CE285A-Cartridge-LaserJet-M1217nfw/dp/B003BFU4TI/ref=sr_1_58?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-58',
    'https://www.amazon.com/Toner-Replacement-M402n-M426fdw-M402/dp/B07PSKZ31X/ref=sr_1_59?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-59',
    'https://www.amazon.com/IKONG-Compatible-Replacement-MFC-9330CDW-MFC-9340CDW/dp/B071R7NCZ8/ref=sr_1_60?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-60',
    'https://www.amazon.com/HP-CF283A-Cartridge-LaserJet-M201dw/dp/B00FW1N1IU/ref=sr_1_61?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-61',
    'https://www.amazon.com/INK-SALE-Replacement-MFC-L2700DW-DCP-L2540DW/dp/B00OT7B6MG/ref=sr_1_62?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-62',
    'https://www.amazon.com/HP-CF502A-Cartridge-LaserJet-M281cdw/dp/B074KSYH38/ref=sr_1_63?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-63',
    'https://www.amazon.com/GPC-Image-Cartridge-045H-CRG-045/dp/B07KR9ZK3Q/ref=sr_1_64?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-64',
    'https://www.amazon.com/HP-CF230A-Black-Cartridge-Laserjet/dp/B01MFDG7GB/ref=sr_1_65?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-65',
    'https://www.amazon.com/JARBO-Compatible-Cartridges-Replacement-Laserjet/dp/B07VQYWXNN/ref=sr_1_66?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-66',
    'https://www.amazon.com/HP-CF410A-CF411A-Cartridges-Magenta/dp/B07QMBHSGM/ref=sr_1_67?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-67',
    'https://www.amazon.com/ejet-Replacement-MFC-L2700DW-DCP-L2540DW-MFC-L2720DW/dp/B07PCQXGQW/ref=sr_1_68?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-68',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg2_1?ie=UTF8&amp;adId=A06118533FSPUIK83PN5P&amp;url=%2FCMCMCM-Remanufactured-Cartridge-OfficeJet-DeskJet%2Fdp%2FB07FCFVGNK%2Fref%3Dsr_1_69_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550207%26sr%3D8-69-spons%26psc%3D1&amp;qualifier=1575550206&amp;id=420249696206537&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg2_2?ie=UTF8&amp;adId=A0266277UGB0G4T6MKAC&amp;url=%2FCompatible-Cartridge-2xCLT-K406S-TG-Imaging%2Fdp%2FB07V49SX64%2Fref%3Dsr_1_70_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550207%26sr%3D8-70-spons%26psc%3D1&amp;qualifier=1575550206&amp;id=420249696206537&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg2_3?ie=UTF8&amp;adId=A029067329XSLOFABGG3C&amp;url=%2FCompatible-Cartridge-TG-Imaging-2xCLT-K504S%2Fdp%2FB07TK4NZWL%2Fref%3Dsr_1_71_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550207%26sr%3D8-71-spons%26psc%3D1&amp;qualifier=1575550206&amp;id=420249696206537&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg2_4?ie=UTF8&amp;adId=A06954672CXNUO1S8NA2E&amp;url=%2FPrint-Save-Repeat-Lexmark-T650H80G-Remanufactured-Cartridge%2Fdp%2FB004YUIO1O%2Fref%3Dsr_1_72_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550207%26sr%3D8-72-spons%26psc%3D1&amp;qualifier=1575550206&amp;id=420249696206537&amp;widgetName=sp_mtf',
    'https://www.amazon.com/Amstech-Compatible-Cartridge-Replacement-Laserjet/dp/B07VJFR871/ref=sr_1_73?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-73',
    'https://www.amazon.com/Original-Canon-Toner-Magenta-Yellow/dp/B00SGTY3P0/ref=sr_1_74?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-74',
    'https://www.amazon.com/HP-LaserJet-Wireless-Printer-W2G51A/dp/B079QRKWLX/ref=sr_1_75?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-75',
    'https://www.amazon.com/RETCH-Brother-TN221-Toner-Replacement/dp/B07TKJRTNJ/ref=sr_1_76?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-76',
    'https://www.amazon.com/Dell-CVXGF-Toner-Cartridge-E310/dp/B00YO6VFQO/ref=sr_1_77?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-77',
    'https://www.amazon.com/Z-Ink-Compatible-Cartridge-Replacement/dp/B07BS4TYRM/ref=sr_1_78?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-78',
    'https://www.amazon.com/Canon-Toner-Cartridge-055-imageCLASS/dp/B07QJDC19D/ref=sr_1_79?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-79',
    'https://www.amazon.com/CMYBabee-Compatible-Replacement-M281fdw-M281cdw/dp/B07RSZNB8W/ref=sr_1_80?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-80',
    'https://www.amazon.com/Compatible-Replacement-HL-3170CDW-MFC-9130CW-MFC-9330CDW/dp/B07BNLKVTZ/ref=sr_1_81?keywords=printer+toner&amp;qid=1575550207&amp;smid=AJ6UUBZ4XPZ9E&amp;sr=8-81',
    'https://www.amazon.com/Dell-WM2JC-Cartridge-C1765nfw-Printers/dp/B00AWLANBI/ref=sr_1_82?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-82',
    'https://www.amazon.com/Z-Ink-Replacement-Brother-TN450/dp/B00NQFJ8TU/ref=sr_1_83?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-83',
    'https://www.amazon.com/Pantum-Monochrome-Wireless-Networking-Printing/dp/B018VN0PTI/ref=sr_1_84?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-84',
    'https://www.amazon.com/Do-Wiser-Replacement-MFC-9340CDW-MFC-9330CDW/dp/B00JAONWR0/ref=sr_1_85?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-85',
    'https://www.amazon.com/Canon-052-High-Capacity-Toner/dp/B07BFF62Y5/ref=sr_1_86?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-86',
    'https://www.amazon.com/Jofoce-Replacement-MFC-L2700DW-DCP-L2540DW-MFC-L2740DW/dp/B07GWJVYN4/ref=sr_1_87?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-87',
    'https://www.amazon.com/Canon-046-Capacity-Cartridge-Packaging/dp/B06XXKNV2T/ref=sr_1_88?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-88',
    'https://www.amazon.com/Compatible-131X-CF210X-Toner-Cartridge/dp/B07CPHNJL9/ref=sr_1_89?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-89',
    'https://www.amazon.com/LxTek-Cartridge-760-HL-L2370DW-HL-L2390DW/dp/B07H655CPT/ref=sr_1_90?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-90',
    'https://www.amazon.com/Dell-Computer-2MMJP-Cartridge-Printers/dp/B0041DXUG8/ref=sr_1_91?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-91',
    'https://www.amazon.com/Brother-TN431BK-Standard-Toner-Retail-Packaging/dp/B06XCD91NC/ref=sr_1_92?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-92',
    'https://www.amazon.com/Canon-Cartridge-Black-High-Capacity/dp/B06Y1MW1FR/ref=sr_1_93?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-93',
    'https://www.amazon.com/GPC-Image-Compatible-Replacement-ImageClass/dp/B07VT2GCRK/ref=sr_1_94?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-94',
    'https://www.amazon.com/CMTOP-Compatible-SL-M2835DW-SL-M2825DW-SL-M2875FW/dp/B07B8K3L9H/ref=sr_1_95?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-95',
    'https://www.amazon.com/Knot-What-Think-Quilting-Mystery-ebook/dp/B01M8OZL19/ref=sr_1_96?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-96',
    'https://www.amazon.com/Brother-Cartridge-4-Pack-Magenta-Yellow/dp/B0048UH2YA/ref=sr_1_97?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-97',
    'https://www.amazon.com/Arthur-Imaging-TN227-MFC-L3750CDW-MFC-L3770CDW/dp/B07LGWLLSC/ref=sr_1_98?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-98',
    'https://www.amazon.com/Brother-Genuine-Yield-Cartridge-TN360/dp/B001167XXY/ref=sr_1_99?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-99',
    'https://www.amazon.com/Genuine-Xerox-Capacity-Cartridge-106R04347/dp/B07VV6QS5M/ref=sr_1_100?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-100',
    'https://www.amazon.com/Dell-PK492-Black-Cartridge-Printer/dp/B002RDPHDI/ref=sr_1_101?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-101',
    'https://www.amazon.com/GPC-Image-Compatible-Cartridge-replacement/dp/B07BS9MMB5/ref=sr_1_102?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-102',
    'https://www.amazon.com/Hitze-Compatible-Cartridge-Replacement-DCP-L2540DW/dp/B07CJZG6F4/ref=sr_1_103?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-103',
    'https://www.amazon.com/Valuetoner-Replacement-TN760-TN-760-DCP-L2550DW/dp/B07TLL8F94/ref=sr_1_104?keywords=printer+toner&amp;qid=1575550207&amp;sr=8-104',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg2_1?ie=UTF8&amp;adId=A044620516W48P6KN48D3&amp;url=%2FClearprint-Compatible-Cartridge-Replacement-Standard%2Fdp%2FB00HZO47S0%2Fref%3Dsr_1_105_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550207%26sr%3D8-105-spons%26psc%3D1&amp;qualifier=1575550206&amp;id=420249696206537&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg2_2?ie=UTF8&amp;adId=A02902051TEJH0WPOMQG1&amp;url=%2FImaging-1XCLT-K406S-1XCLT-C406S-1XCLT-Y406S-1XCLT-M406S%2Fdp%2FB07V25SPQX%2Fref%3Dsr_1_106_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550207%26sr%3D8-106-spons%26psc%3D1&amp;qualifier=1575550206&amp;id=420249696206537&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg2_3?ie=UTF8&amp;adId=A03281642EQKEPMJ7FL4S&amp;url=%2FMYTONER-Remanufactured-Cartridge-Replacement-Tri-Color%2Fdp%2FB07NK7ZDH8%2Fref%3Dsr_1_107_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550207%26sr%3D8-107-spons%26psc%3D1&amp;qualifier=1575550206&amp;id=420249696206537&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg2_4?ie=UTF8&amp;adId=A031517615SCIBS9Q20IC&amp;url=%2FMYTONER-Compatible-Cartridge-Replacement-LBP622Cdw%2Fdp%2FB07WCVNVWD%2Fref%3Dsr_1_108_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550207%26sr%3D8-108-spons%26psc%3D1&amp;qualifier=1575550206&amp;id=420249696206537&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg3_1?ie=UTF8&amp;adId=A10221222Q90U0UA10OK0&amp;url=%2FMYTONER-Re-Manufactured-Cartridge-Replacement-Tri-Color%2Fdp%2FB0792TPLWQ%2Fref%3Dsr_1_97_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550208%26sr%3D8-97-spons%26psc%3D1&amp;qualifier=1575550208&amp;id=2620934486296898&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg3_2?ie=UTF8&amp;adId=A09763873P8XNZN6KFX0F&amp;url=%2FMYTONER-Re-Manufactured-Cartridge-Replacement-PG-245XL%2Fdp%2FB07GNBG9TY%2Fref%3Dsr_1_98_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550208%26sr%3D8-98-spons%26psc%3D1&amp;qualifier=1575550208&amp;id=2620934486296898&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg3_3?ie=UTF8&amp;adId=A04731622ZM2CXEC5FI3H&amp;url=%2FTG-Imaging-Compatible-Replacement-DCP-8110DN%2Fdp%2FB06ZYJD4QJ%2Fref%3Dsr_1_99_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550208%26sr%3D8-99-spons%26psc%3D1&amp;qualifier=1575550208&amp;id=2620934486296898&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg3_4?ie=UTF8&amp;adId=A0994105VEJZIN3KD85R&amp;url=%2FLCL-Compatible-Cartridge-Replacement-593-BBYO%2Fdp%2FB07DXQFQS5%2Fref%3Dsr_1_100_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550208%26sr%3D8-100-spons%26psc%3D1&amp;qualifier=1575550208&amp;id=2620934486296898&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/GPC-Image-Remanufactured-Replacement-ImageClass/dp/B07QV8P651/ref=sr_1_101?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-101',
    'https://www.amazon.com/Cool-Toner-80A-CF280A-CF280X/dp/B07H8RWDCQ/ref=sr_1_102?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-102',
    'https://www.amazon.com/Brother-Cartridge-TN820-Replacement-Replenishment/dp/B01825OFNC/ref=sr_1_103?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-103',
    'https://www.amazon.com/Ink-Replacement-MFC-L3750CDW-MFC-L3770CDW-Black/dp/B07JLJSZRM/ref=sr_1_104?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-104',
    'https://www.amazon.com/Shidono-Toner-Replacement-305X-305A/dp/B07S738217/ref=sr_1_105?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-105',
    'https://www.amazon.com/Arcon-Replacement-MFC-L2710DW-DCP-L2550DW-MFC-l2750dw/dp/B07S1R4DQZ/ref=sr_1_106?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-106',
    'https://www.amazon.com/HP-Cartridge-Cartridges-CE505D-LaserJet/dp/B005DWUOXI/ref=sr_1_107?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-107',
    'https://www.amazon.com/Arcon-Compatible-Replacement-48A-CF248A/dp/B07SXRZXJQ/ref=sr_1_108?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-108',
    'https://www.amazon.com/Arcon-TN850-TN-850-TN820-TN-820/dp/B07HGYSTQH/ref=sr_1_109?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-109',
    'https://www.amazon.com/LINKYO-Compatible-Cartridge-Replacement-Brother/dp/B07FPXRPXM/ref=sr_1_110?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-110',
    'https://www.amazon.com/JARBO-Replacement-DCP-L2540DW-DCP-L2520DW-MFC-L2700DW/dp/B01BY76BPU/ref=sr_1_111?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-111',
    'https://www.amazon.com/STAROVER-Compatible-Cartridges-Replacement-SL-M2070FW/dp/B075M8YX5N/ref=sr_1_112?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-112',
    'https://www.amazon.com/Cool-Toner-HL-L8360CDWT-MFC-L8900CDW-MFC-L8610CDW/dp/B07B2TKVJ5/ref=sr_1_113?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-113',
    'https://www.amazon.com/Canon-imageCLASS-MF236n-Mobile-Printer/dp/B01K1KUQHK/ref=sr_1_114?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-114',
    'https://www.amazon.com/Brother-Cartridge-TN221C-Replacement-Replenishment/dp/B00BR3WX7W/ref=sr_1_115?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-115',
    'https://www.amazon.com/Compatible-Cartridge-Replacement-ImageCLASS-LBP612Cdw/dp/B07MVXHJKF/ref=sr_1_116?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-116',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg3_1?ie=UTF8&amp;adId=A02849913PE046WJTU4G4&amp;url=%2FLCL-Compatible-Cartridge-Replacement-CF362A%2Fdp%2FB07CN3KJFB%2Fref%3Dsr_1_117_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550208%26sr%3D8-117-spons%26psc%3D1%26smid%3DA15P6DOGPNMGGZ&amp;qualifier=1575550208&amp;id=2620934486296898&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg3_2?ie=UTF8&amp;adId=A000873433AEUHP43N1XP&amp;url=%2FPrint-Save-Repeat-03YNJ-Extra-Remanufactured-Cartridge%2Fdp%2FB00FOVHHR4%2Fref%3Dsr_1_118_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550208%26sr%3D8-118-spons%26psc%3D1&amp;qualifier=1575550208&amp;id=2620934486296898&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg3_3?ie=UTF8&amp;adId=A09775632CLGR9NXMOKW5&amp;url=%2FOCProducts-Refilled-Cartridge-Replacement-Officejet%2Fdp%2FB01NA7GTUB%2Fref%3Dsr_1_119_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550208%26sr%3D8-119-spons%26psc%3D1&amp;qualifier=1575550208&amp;id=2620934486296898&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg3_4?ie=UTF8&amp;adId=A06934771M8TBK9USH8DB&amp;url=%2FLCL-Compatible-Cartridge-Replacement-S2825cdn%2Fdp%2FB0796T2S65%2Fref%3Dsr_1_120_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550208%26sr%3D8-120-spons%26psc%3D1&amp;qualifier=1575550208&amp;id=2620934486296898&amp;widgetName=sp_mtf',
    'https://www.amazon.com/C3903A-LaserJet-Cartridge-DISCONTINUED-MANUFACTURER/dp/B00000J0RE/ref=sr_1_121?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-121',
    'https://www.amazon.com/IKONG-Compatible-593-BBKD-Cartridge-Printer/dp/B075CPXXM5/ref=sr_1_122?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-122',
    'https://www.amazon.com/ZIPRINT-Compatible-Replacement-94A-CF294A/dp/B07QCT41LH/ref=sr_1_123?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-123',
    'https://www.amazon.com/IKONG-Compatible-Replacement-MFC-9330CDW-MFC-9340CDW/dp/B07S4DT9PY/ref=sr_1_124?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-124',
    'https://www.amazon.com/Cool-Toner-HL-L8360CDWT-MFC-L8900CDW-MFC-L8610CDW/dp/B01CEBY2GU/ref=sr_1_125?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-125',
    'https://www.amazon.com/GPC-Image-Compatible-Replacement-ImageCLASS/dp/B07SL1FRX1/ref=sr_1_126?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-126',
    'https://www.amazon.com/Do-Wiser-Compatible-C1760nw-C1765nfw/dp/B01M0PKHY9/ref=sr_1_127?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-127',
    'https://www.amazon.com/Z-Ink-Compatible-Cartridge-Replacement/dp/B077RV47SM/ref=sr_1_128?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-128',
    'https://www.amazon.com/V4INK-Replacement-MFC-L2700DW-DCP-L2540DW-MFC-L2720DW/dp/B00NOFNXU2/ref=sr_1_129?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-129',
    'https://www.amazon.com/Z-Ink-Compatible-Cartridge-Replacement/dp/B0777Y4QYQ/ref=sr_1_130?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-130',
    'https://www.amazon.com/Cool-Toner-Compatible-Replacement-CLX-4195fw/dp/B01J7OOMKS/ref=sr_1_131?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-131',
    'https://www.amazon.com/MLT-D111S-MLT-D111L-7Magic-Compatible-Toner/dp/B06XDYCBMW/ref=sr_1_132?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-132',
    'https://www.amazon.com/LxTek-Compatible-Cartridge-Replacement-137/dp/B078JT61Y8/ref=sr_1_133?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-133',
    'https://www.amazon.com/Valuetoner-Compatible-Cartridge-Replacement-Laserjet/dp/B07D2BQZNY/ref=sr_1_134?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-134',
    'https://www.amazon.com/Arcon-Compatible-Cartridge-Replacement-Laserjet/dp/B07P5WHLG5/ref=sr_1_135?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-135',
    'https://www.amazon.com/GREENSKY-Toner-Cartridge-Replacement-M281fdw/dp/B07SX2B62X/ref=sr_1_136?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-136',
    'https://www.amazon.com/HP-CF400X-Cartridge-Laserjet-M252dw/dp/B00UBMO61G/ref=sr_1_137?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-137',
    'https://www.amazon.com/Kogain-Replacement-HL-L2370DWXL-DCP-L2550DW-MFC-L2750DW/dp/B07SPJJ3Y8/ref=sr_1_138?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-138',
    'https://www.amazon.com/Compatible-Cartridge-Replacement-Laserjet-M479fdw/dp/B07ZZ59PQP/ref=sr_1_139?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-139',
    'https://www.amazon.com/LxTek-Compatible-Cartridge-Replacement-593-BBJX/dp/B077P4WXM1/ref=sr_1_140?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-140',
    'https://www.amazon.com/EBY-Replacement-MFC-L2700DW-MFC-L2720DW-MFC-L2740DW/dp/B075HC37XV/ref=sr_1_141?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-141',
    'https://www.amazon.com/GREENSKY-Compatible-Cartridge-Replacement-Laserjet/dp/B07KXMKKB8/ref=sr_1_142?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-142',
    'https://www.amazon.com/V4INK-Compatible-Replacement-Cartridge-Laserjet/dp/B07FKHNPYN/ref=sr_1_143?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-143',
    'https://www.amazon.com/LxTek-Replacement-202X-202A-M254dw/dp/B07TYTLCR4/ref=sr_1_144?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-144',
    'https://www.amazon.com/Arcon-410A-M477fnw-M477fdn-M477fdw/dp/B07FFHLR75/ref=sr_1_145?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-145',
    'https://www.amazon.com/Z-Ink-Compatible-Cartridge-Replacement/dp/B07782KG6L/ref=sr_1_146?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-146',
    'https://www.amazon.com/Brother-Standard-Cartridge-Replacement-Replenishment/dp/B07FNBQDG4/ref=sr_1_147?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-147',
    'https://www.amazon.com/Do-Wiser-Compatible-Samsung-ProXpress/dp/B017DO8U9S/ref=sr_1_148?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-148',
    'https://www.amazon.com/LINKYO-Compatible-Cartridge-Replacement-Brother/dp/B074VV3QKT/ref=sr_1_149?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-149',
    'https://www.amazon.com/Cartlee-Compatible-Cartridges-Replacement-C1765nfw/dp/B07BSLX3WP/ref=sr_1_150?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-150',
    'https://www.amazon.com/Xerox-Cartridge-Phaser-WorkCentre-106R02720/dp/B00EW4BLPI/ref=sr_1_151?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-151',
    'https://www.amazon.com/Compatible-Cartridge-Replacement-Laserjet-M477fnw/dp/B07MLKG7KG/ref=sr_1_152?keywords=printer+toner&amp;qid=1575550208&amp;sr=8-152',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg3_1?ie=UTF8&amp;adId=A0446105PYE7Q6CBGX5T&amp;url=%2FClearprint-Compatible-MFC-9130CW-MFC-9330CDW-MFC-9340CDW%2Fdp%2FB00HLO2T3O%2Fref%3Dsr_1_153_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550208%26sr%3D8-153-spons%26psc%3D1&amp;qualifier=1575550208&amp;id=2620934486296898&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg3_2?ie=UTF8&amp;adId=A0014317E223RLHOVM02&amp;url=%2FPrint-Save-Repeat-Lexmark-53B1H00-Remanufactured-Cartridge%2Fdp%2FB07BQC2ZTB%2Fref%3Dsr_1_154_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550208%26sr%3D8-154-spons%26psc%3D1&amp;qualifier=1575550208&amp;id=2620934486296898&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg3_3?ie=UTF8&amp;adId=A06161581EHBTT0K7W9RR&amp;url=%2FNew-York-Toner-Compatible-MLT-D118L%2Fdp%2FB01N9DB8IF%2Fref%3Dsr_1_155_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550208%26sr%3D8-155-spons%26psc%3D1&amp;qualifier=1575550208&amp;id=2620934486296898&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg3_4?ie=UTF8&amp;adId=A02200322Z2JT00ZNTVK6&amp;url=%2FGREENSKY-Compatible-Cartridge-Replacement-C1765nfw%2Fdp%2FB07VT1Q5XH%2Fref%3Dsr_1_156_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550208%26sr%3D8-156-spons%26psc%3D1&amp;qualifier=1575550208&amp;id=2620934486296898&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg4_1?ie=UTF8&amp;adId=A0210766291TKHIKRJ3UQ&amp;url=%2FmyCartridge-Compatible-Replacement-MFC-J491DW-MFC-J497DW%2Fdp%2FB07K142CXH%2Fref%3Dsr_1_145_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550209%26sr%3D8-145-spons%26psc%3D1&amp;qualifier=1575550209&amp;id=8352767996462105&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg4_2?ie=UTF8&amp;adId=A017639518CH7RIZKAGMX&amp;url=%2FmyCartridge-Compatible-Replacement-87A-CF287A%2Fdp%2FB07JZBH1T5%2Fref%3Dsr_1_146_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550209%26sr%3D8-146-spons%26psc%3D1&amp;qualifier=1575550209&amp;id=8352767996462105&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg4_3?ie=UTF8&amp;adId=A0466218CK76K2L96TD8&amp;url=%2FINSMAX-Remanufactured-Replacement-Compatible-1Tri-Color%2Fdp%2FB07Q2Y9TW7%2Fref%3Dsr_1_147_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550209%26sr%3D8-147-spons%26psc%3D1&amp;qualifier=1575550209&amp;id=8352767996462105&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg4_4?ie=UTF8&amp;adId=A09265563K5Y3ERPM7YWF&amp;url=%2FRemanufactured-Cartridge-Replacement-Workforce-1Magenta%2Fdp%2FB07GR8RXMQ%2Fref%3Dsr_1_148_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550209%26sr%3D8-148-spons%26psc%3D1&amp;qualifier=1575550209&amp;id=8352767996462105&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/Canon-Original-045-Toner-Cartridge/dp/B06XZ88THM/ref=sr_1_149?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-149',
    'https://www.amazon.com/LxTek-Cartridge-C1760nw-1350cnw-1355cn/dp/B07GFJ9TT8/ref=sr_1_150?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-150',
    'https://www.amazon.com/Valuetoner-Compatible-Replacement-Canon-128/dp/B07GRTNPJF/ref=sr_1_151?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-151',
    'https://www.amazon.com/Cool-Toner-Compatible-85A-Cartridge/dp/B00ENC3UE4/ref=sr_1_152?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-152',
    'https://www.amazon.com/Renewable-Toner-Replacement-CF248A-48A/dp/B07HJD57BR/ref=sr_1_153?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-153',
    'https://www.amazon.com/myCartridge-Compatible-Cartridge-Replacement-Laserjet/dp/B078MLSFXM/ref=sr_1_154?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-154',
    'https://www.amazon.com/CLT-K504S-Cartridge-SL-C1810W-CLX-4195N-CLP-415N/dp/B008HSIXJC/ref=sr_1_155?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-155',
    'https://www.amazon.com/Original-Laserjet-Cartridge-CF500A-CF501A/dp/B081177GZG/ref=sr_1_156?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-156',
    'https://www.amazon.com/Ink-Replacement-TN227-MFC-L3750CDW-MFC-L3770CDW/dp/B07JKNXTRN/ref=sr_1_157?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-157',
    'https://www.amazon.com/Samsung-MLT-D116S-Cartridge-SL-M2625D-2825DW/dp/B00C2AM27A/ref=sr_1_158?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-158',
    'https://www.amazon.com/Compatible-LaserJet-M477fdn-M477fnw-M477fdw/dp/B0037BYL5O/ref=sr_1_159?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-159',
    'https://www.amazon.com/HP-CE255A-Original-Cartridge-Enterprise/dp/B002EDLQRW/ref=sr_1_160?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-160',
    'https://www.amazon.com/Arcon-Compatible-Cartridge-Replacement-LaserJet/dp/B07T45PLH1/ref=sr_1_161?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-161',
    'https://www.amazon.com/Brother-Standard-Cartridge-Replacement-Replenishment/dp/B07TNH2TQK/ref=sr_1_162?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-162',
    'https://www.amazon.com/GPC-Image-Compatible-Replacement-17A/dp/B07KCDXKFD/ref=sr_1_163?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-163',
    'https://www.amazon.com/Inktoneram-Replacement-cartridges-Cartridge-replacement/dp/B00AVBGICM/ref=sr_1_164?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-164',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg4_1?ie=UTF8&amp;adId=A02078282OQSVL3XKPWJ7&amp;url=%2FToner-Tap-Versalink-Printers-Bundle%2Fdp%2FB07NY5CWNN%2Fref%3Dsr_1_165_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550209%26sr%3D8-165-spons%26psc%3D1&amp;qualifier=1575550209&amp;id=8352767996462105&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg4_2?ie=UTF8&amp;adId=A07553942DRRY0VXVRH6B&amp;url=%2FMagenta-Cartridges-Printer-Compatible-C1760nw%2Fdp%2FB06ZYLHHYP%2Fref%3Dsr_1_166_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550209%26sr%3D8-166-spons%26psc%3D1&amp;qualifier=1575550209&amp;id=8352767996462105&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg4_3?ie=UTF8&amp;adId=A09385272MJODG1Q3C3QI&amp;url=%2FPrint-Save-Repeat-Lexmark-Extra-Remanufactured-Cartridge%2Fdp%2FB00FSKYE22%2Fref%3Dsr_1_167_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550209%26sr%3D8-167-spons%26psc%3D1&amp;qualifier=1575550209&amp;id=8352767996462105&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg4_4?ie=UTF8&amp;adId=A088805623ZZ89IBJSJH1&amp;url=%2FMYTONER-Remanufactured-Replacement-125A-CP1215%2Fdp%2FB07TXQ8ZBV%2Fref%3Dsr_1_168_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550209%26sr%3D8-168-spons%26psc%3D1&amp;qualifier=1575550209&amp;id=8352767996462105&amp;widgetName=sp_mtf',
    'https://www.amazon.com/Canon-Original-126-Toner-Cartridge/dp/B00J4C533E/ref=sr_1_169?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-169',
    'https://www.amazon.com/Z-Ink-Compatible-Cartridge-Replacement/dp/B07BS856CD/ref=sr_1_170?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-170',
    'https://www.amazon.com/MYTONER-Compatible-Cartridge-Replacement-imageCLASS/dp/B07XC6N95M/ref=sr_1_171?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-171',
    'https://www.amazon.com/LxTek-Compatible-Replacement-SL-M2830DW-SL-M2880FW/dp/B07BRWXKKV/ref=sr_1_172?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-172',
    'https://www.amazon.com/HP-Cartridge-Cartridges-CE285D-LaserJet/dp/B006588NGY/ref=sr_1_173?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-173',
    'https://www.amazon.com/Speedy-Inks-Remanufactured-Cartridge-Replacement/dp/B00KANT6JI/ref=sr_1_174?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-174',
    'https://www.amazon.com/Canon-Original-125-Toner-Cartridge/dp/B00MFNXKDY/ref=sr_1_175?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-175',
    'https://www.amazon.com/Brother-Cartridge-TN221M-Replacement-Replenishment/dp/B00BR3WXS6/ref=sr_1_176?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-176',
    'https://www.amazon.com/HP-CF230X-Black-Cartridge-Laserjet/dp/B01MQ2GI8J/ref=sr_1_177?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-177',
    'https://www.amazon.com/LxTek-Cartridge-137-9435B001AA-D570/dp/B01GHQC6AW/ref=sr_1_178?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-178',
    'https://www.amazon.com/JARBO-Compatible-Cartridges-Replacement-Laserjet/dp/B06XKNQJP3/ref=sr_1_179?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-179',
    'https://www.amazon.com/Ink-Replacement-MFC-9330CDW-MFC-9340CDW-DCP-9020CDN/dp/B00JFAAH40/ref=sr_1_180?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-180',
    'https://www.amazon.com/cartridge-emphasis-re-manufactured-compatible-cartridges-ebook/dp/B07C3QVMZY/ref=sr_1_181?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-181',
    'https://www.amazon.com/Compatible-CLT-K504S-Cartridge-CLX-4195FW-ColorPrint/dp/B07S1M4LJL/ref=sr_1_182?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-182',
    'https://www.amazon.com/Ricoh-Black-Toner-Cartridge-407539/dp/B010239PW8/ref=sr_1_183?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-183',
    'https://www.amazon.com/Do-Wiser-Compatible-S2825cdn-593-BBOW/dp/B01E5PY77M/ref=sr_1_184?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-184',
    'https://www.amazon.com/HP-CF281A-Cartridge-LaserJet-Enterprise/dp/B00MCDK9MM/ref=sr_1_185?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-185',
    'https://www.amazon.com/OfficeWorld-P1102w-P1109w-M1212nf-M1217nfw/dp/B01LWLG44Z/ref=sr_1_186?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-186',
    'https://www.amazon.com/HP-Q2612A-Original-Cartridge-LaserJet/dp/B0000C120T/ref=sr_1_187?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-187',
    'https://www.amazon.com/Arcon-Compatible-Cartridge-Replacement-ImageCLASS/dp/B07VG8QYXQ/ref=sr_1_188?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-188',
    'https://www.amazon.com/Print-Save-Repeat-PK941-Yield-Remanufactured-Cartridge/dp/B008CPIKH0/ref=sr_1_189?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-189',
    'https://www.amazon.com/Valuetoner-Compatible-Cartridge-Replacement-LaserJet/dp/B07D2BBT7C/ref=sr_1_190?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-190',
    'https://www.amazon.com/HP-CF280X-Black-Cartridge-LaserJet/dp/B007RHU1PS/ref=sr_1_191?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-191',
    'https://www.amazon.com/Cartridge-CLT-K404S-CLT-C404S-CLT-M404S-CLT-Y404S/dp/B0784P3WV3/ref=sr_1_192?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-192',
    'https://www.amazon.com/LxTek-Compatible-Cartridge-Replacement-LaserJet/dp/B01CPH2IIM/ref=sr_1_193?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-193',
    'https://www.amazon.com/HP-CE278A-Cartridge-Cartridges-CE278D/dp/B006588N5U/ref=sr_1_194?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-194',
    'https://www.amazon.com/Ink-Replacement-Brother-TN221-TN225/dp/B00JFAFETS/ref=sr_1_195?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-195',
    'https://www.amazon.com/Xerox-Standard-Capacity-Cartridge-106R03620/dp/B01L959SMA/ref=sr_1_196?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-196',
    'https://www.amazon.com/Brother-HL-L2300D-Monochrome-Printer-Printing/dp/B00NQ1CLTI/ref=sr_1_197?keywords=printer+toner&amp;qid=1575550209&amp;smid=ATVPDKIKX0DER&amp;sr=8-197',
    'https://www.amazon.com/Brother-Printer-TN433BK-Toner-Retail-Packaging/dp/B06XDQVJ28/ref=sr_1_198?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-198',
    'https://www.amazon.com/JARBO-Compatible-Cartridges-Replacement-MLT-D111S/dp/B01BYBMUNI/ref=sr_1_199?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-199',
    'https://www.amazon.com/HP-CF501A-Cartridge-LaserJet-M281cdw/dp/B074KTXNZF/ref=sr_1_200?keywords=printer+toner&amp;qid=1575550209&amp;sr=8-200',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg4_1?ie=UTF8&amp;adId=A0864867ULF0V57EHIR5&amp;url=%2FDCP-L5500DN-DCP-L5650DN-HL-L6200DWT-MFC-L5800DW-EasyPrint%2Fdp%2FB07VDCSGTQ%2Fref%3Dsr_1_201_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550209%26sr%3D8-201-spons%26psc%3D1&amp;qualifier=1575550209&amp;id=8352767996462105&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg4_2?ie=UTF8&amp;adId=A0341935WC7XJ5OUODPM&amp;url=%2FCompatible-CLT-K406S-Cartridge-CLX-3306FN-EasyPrint%2Fdp%2FB07QLXY26V%2Fref%3Dsr_1_202_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550209%26sr%3D8-202-spons%26psc%3D1&amp;qualifier=1575550209&amp;id=8352767996462105&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg4_3?ie=UTF8&amp;adId=A0290273SLPO6NCKDPH3&amp;url=%2FTG-Imaging-Compatible-MLT-D111S-Cartridge%2Fdp%2FB07TS4TSLY%2Fref%3Dsr_1_203_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550209%26sr%3D8-203-spons%26psc%3D1&amp;qualifier=1575550209&amp;id=8352767996462105&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg4_4?ie=UTF8&amp;adId=A01527353EE7SE2315X4Q&amp;url=%2FCMCMCM-Compatible-Cartridges-Replacements-MFC9330CDW%2Fdp%2FB07BPWX5X4%2Fref%3Dsr_1_204_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550209%26sr%3D8-204-spons%26psc%3D1&amp;qualifier=1575550209&amp;id=8352767996462105&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg5_1?ie=UTF8&amp;adId=A07355112BAOZMKK2IACK&amp;url=%2FOCProducts-Refilled-Cartridge-Replacement-Printers%2Fdp%2FB01M4S2I67%2Fref%3Dsr_1_193_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550211%26sr%3D8-193-spons%26psc%3D1&amp;qualifier=1575550211&amp;id=3484599039813543&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg5_2?ie=UTF8&amp;adId=A0525383GDZZD460RJVT&amp;url=%2FReplacement-DCP-L2540DW-MFC-L2700DW-MFC-L2740DW-DCP-L2520DW%2Fdp%2FB01H1SQDJU%2Fref%3Dsr_1_194_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550211%26sr%3D8-194-spons%26psc%3D1&amp;qualifier=1575550211&amp;id=3484599039813543&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg5_3?ie=UTF8&amp;adId=A03520712I0U7AECF61GP&amp;url=%2FToner-Refill-Store-Replacment-Compatible%2Fdp%2FB00DYZJ7TI%2Fref%3Dsr_1_195_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550211%26sr%3D8-195-spons%26psc%3D1&amp;qualifier=1575550211&amp;id=3484599039813543&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg5_4?ie=UTF8&amp;adId=A08367071I7KM1X98ZIMB&amp;url=%2FLexmark-MB2338adw-Monochrome-Printing-36SC640%2Fdp%2FB07F21DSM8%2Fref%3Dsr_1_196_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550211%26sr%3D8-196-spons%26psc%3D1&amp;qualifier=1575550211&amp;id=3484599039813543&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/BAISINE-Compatible-Cartridge-Replacement-S2830dn/dp/B07QFQVHHQ/ref=sr_1_197?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-197',
    'https://www.amazon.com/Arcon-Toner-Cartridge-Replacement-131/dp/B00V9KZ9LU/ref=sr_1_198?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-198',
    'https://www.amazon.com/MLT-D205L-Cartridge-ML-3312ND-SCX-4835FR-SCX-5639FR/dp/B004H602WO/ref=sr_1_199?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-199',
    'https://www.amazon.com/HP-Q5949A-Black-Original-Cartridge/dp/B00061RWQS/ref=sr_1_200?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-200',
    'https://www.amazon.com/TG-Imaging-Compatible-Replacement-Laserjet/dp/B07L19BR4F/ref=sr_1_201?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-201',
    'https://www.amazon.com/STAROVER-Compatible-Cartridges-Replacement-CLX-3305FW/dp/B075M6QS65/ref=sr_1_202?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-202',
    'https://www.amazon.com/LinkToner-Compatible-Cartridge-Replacement-Brother/dp/B07B26QWKZ/ref=sr_1_203?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-203',
    'https://www.amazon.com/LINKYO-Compatible-Cartridge-Replacement-Brother/dp/B0051MT1HU/ref=sr_1_204?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-204',
    'https://www.amazon.com/JARBO-Compatible-Cartridges-SCX-4623FW-SCX-4623FN/dp/B075KMPHLW/ref=sr_1_205?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-205',
    'https://www.amazon.com/HIINK-Replacement-DCP-L2520DW-DCP-L2540DW-MFC-L2700DW/dp/B075VDJWDV/ref=sr_1_206?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-206',
    'https://www.amazon.com/TEINO-Compatible-Cartridge-Replacement-Laserjet/dp/B07VMLBVFM/ref=sr_1_207?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-207',
    'https://www.amazon.com/Z-Ink-Compatible-Replacement-MFC-7860DW/dp/B00J8ULNPO/ref=sr_1_208?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-208',
    'https://www.amazon.com/Valuetoner-Compatible-Replacement-202X-CF500X/dp/B07TT91WX7/ref=sr_1_209?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-209',
    'https://www.amazon.com/HP-CE410A-Original-Cartridge-LaserJet/dp/B006ZZGDH8/ref=sr_1_210?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-210',
    'https://www.amazon.com/TG-Imaging-Compatible-MLT-D111S-Cartridge/dp/B07TS4TSLY/ref=sr_1_211?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-211',
    'https://www.amazon.com/Arcon-Toner-M402n-M402dn-M402dw/dp/B07BGXTNNP/ref=sr_1_212?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-212',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg5_1?ie=UTF8&amp;adId=A02798072N12Q9AB1LIIW&amp;url=%2FCompatible-Cartridge-Laserjet-Printer-EasyPrint%2Fdp%2FB07VMK5Q9L%2Fref%3Dsr_1_213_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550211%26sr%3D8-213-spons%26psc%3D1&amp;qualifier=1575550211&amp;id=3484599039813543&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg5_2?ie=UTF8&amp;adId=A100910835MNW80LEACRV&amp;url=%2FToner-Tap-Versalink-Printer-Bundle%2Fdp%2FB07NSHLRH6%2Fref%3Dsr_1_214_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550211%26sr%3D8-214-spons%26psc%3D1&amp;qualifier=1575550211&amp;id=3484599039813543&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg5_3?ie=UTF8&amp;adId=A0037373QKEDV60VWGLS&amp;url=%2FHIINK-Comaptible-Cartridge-Replacement-Laserjet%2Fdp%2FB01B71HKW6%2Fref%3Dsr_1_215_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550211%26sr%3D8-215-spons%26psc%3D1&amp;qualifier=1575550211&amp;id=3484599039813543&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg5_4?ie=UTF8&amp;adId=A02353683SHRLPLNVR6Q8&amp;url=%2FSherman-Inks-Capacity-PGI-220-Cartridge%2Fdp%2FB07665MK2Z%2Fref%3Dsr_1_216_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550211%26sr%3D8-216-spons%26psc%3D1&amp;qualifier=1575550211&amp;id=3484599039813543&amp;widgetName=sp_mtf',
    'https://www.amazon.com/HP-CF360A-Original-Cartridge-Enterprise/dp/B00UBMOD1O/ref=sr_1_217?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-217',
    'https://www.amazon.com/HP-58A-CF258A-Toner-Cartridge/dp/B07QZ4ZKYG/ref=sr_1_218?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-218',
    'https://www.amazon.com/Toner-Bank-Replacement-M281fdw-M254dw/dp/B07VHYFXZV/ref=sr_1_219?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-219',
    'https://www.amazon.com/Dell-2RF0R-Yellow-Toner-Cartridge/dp/B0179JVOPE/ref=sr_1_220?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-220',
    'https://www.amazon.com/Brother-Cartridge-TN720-Replacement-Replenishment/dp/B0084JMC9G/ref=sr_1_221?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-221',
    'https://www.amazon.com/4Benefit-Compatible-Cartridge-Replacement-Laserjet/dp/B07MMJ5MNT/ref=sr_1_222?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-222',
    'https://www.amazon.com/CMYBabee-Compatible-Cartridge-Replacement-Cartridges/dp/B07TC1NHJ2/ref=sr_1_223?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-223',
    'https://www.amazon.com/Toner-Cartridge-Replacement-046-MF733Cdw/dp/B07PHRP7DB/ref=sr_1_224?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-224',
    'https://www.amazon.com/Brother-Cartridge-TN880-Replacement-Replenishment/dp/B01825OHX0/ref=sr_1_225?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-225',
    'https://www.amazon.com/PB-211-Cartridge-Pantum-M6550NW-M6600NW/dp/B07FYY1D9B/ref=sr_1_226?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-226',
    'https://www.amazon.com/Do-Wiser-Compatible-Cartridge-Replacement/dp/B07NF1B6HP/ref=sr_1_227?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-227',
    'https://www.amazon.com/Canon-Original-104-Toner-Cartridge/dp/B000B02BEM/ref=sr_1_228?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-228',
    'https://www.amazon.com/MYTONER-Compatible-Cartridge-Replacement-LBP622Cdw/dp/B07WCVNVWD/ref=sr_1_229?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-229',
    'https://www.amazon.com/Canon-Toner-Cartridge-054-imageCLASS/dp/B07QH3C22R/ref=sr_1_230?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-230',
    'https://www.amazon.com/Aztech-Compatible-Cartridge-Replacement-Magenta/dp/B07N397D36/ref=sr_1_231?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-231',
    'https://www.amazon.com/Compatible-Brother-TN-660-TN-630-Cartridge/dp/B075SKT8WM/ref=sr_1_232?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-232',
    'https://www.amazon.com/MYTONER-Brother-TN227-HL-L3230CDW-MFC-L3710CW/dp/B07SM79JJD/ref=sr_1_233?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-233',
    'https://www.amazon.com/V4INK-Compatible-Cartridge-MFC-7345N-MFC-7440N/dp/B00A02Y2XO/ref=sr_1_234?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-234',
    'https://www.amazon.com/myCartridge-Compatible-Cartridge-Replacement-Brother/dp/B07F65KCHL/ref=sr_1_235?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-235',
    'https://www.amazon.com/TRUE-IMAGE-Compatible-Replacement-ImageCLASS/dp/B07BZ67M22/ref=sr_1_236?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-236',
    'https://www.amazon.com/Z-Ink-Compatible-Replacement-9435B001AA/dp/B01NBB1J9U/ref=sr_1_237?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-237',
    'https://www.amazon.com/Compatible-Replacement-WorkCentre-Toney-King/dp/B07W6NY6KF/ref=sr_1_238?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-238',
    'https://www.amazon.com/Dell-XMX5D-Cartridge-Magenta-Packaging/dp/B00AWL2FB4/ref=sr_1_239?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-239',
    'https://www.amazon.com/GPC-Image-Replacement-MFC-9970CDW-MFC-9460CDN/dp/B01HR59BYQ/ref=sr_1_240?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-240',
    'https://www.amazon.com/Brother-Cartridge-TN221Y-Replacement-Replenishment/dp/B00BR3WYD0/ref=sr_1_241?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-241',
    'https://www.amazon.com/Inktoneram-Replacement-cartridges-Cartridge-replacement/dp/B00AVBGIIQ/ref=sr_1_242?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-242',
    'https://www.amazon.com/Do-Wiser-Compatible-Cartridge-Replacement/dp/B013TESHOE/ref=sr_1_243?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-243',
    'https://www.amazon.com/MIROO-Compatible-Replacement-MFC-7860DW-DCP-7065DN/dp/B075K3VHV4/ref=sr_1_244?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-244',
    'https://www.amazon.com/CMYBabee-Compatible-Replacement-MFC-L2730DW-DCP-L2550DW/dp/B07HF7M5M8/ref=sr_1_245?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-245',
    'https://www.amazon.com/Cool-Toner-Compatible-Cartridge-Replacement/dp/B07MLJBX19/ref=sr_1_246?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-246',
    'https://www.amazon.com/JARBO-Compatible-Cartridge-Replacement-ImageCLASS/dp/B07VNRB8XB/ref=sr_1_247?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-247',
    'https://www.amazon.com/GPC-Image-Compatible-Cartridge-Replacement/dp/B0721SL5V5/ref=sr_1_248?keywords=printer+toner&amp;qid=1575550211&amp;sr=8-248',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg5_1?ie=UTF8&amp;adId=A06887231CQEOO2VVH1SU&amp;url=%2FPrint-Save-Repeat-InfoPrint-39V2513-Remanufactured-Cartridges%2Fdp%2FB005JZRHJS%2Fref%3Dsr_1_249_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550211%26sr%3D8-249-spons%26psc%3D1&amp;qualifier=1575550211&amp;id=3484599039813543&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg5_2?ie=UTF8&amp;adId=A08092651UHMMJD19P55&amp;url=%2FCompatible-054-Replacement-Canon-054H%2Fdp%2FB07R1VMLZG%2Fref%3Dsr_1_250_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550211%26sr%3D8-250-spons%26psc%3D1&amp;qualifier=1575550211&amp;id=3484599039813543&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg5_3?ie=UTF8&amp;adId=A0362136Z2K5K9O24NMS&amp;url=%2FMYTONER-Compatible-Brother-Cartridge-Printers%2Fdp%2FB07S752VQS%2Fref%3Dsr_1_251_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550211%26sr%3D8-251-spons%26psc%3D1&amp;qualifier=1575550211&amp;id=3484599039813543&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg5_4?ie=UTF8&amp;adId=A05833672EJG89X50B9LY&amp;url=%2FCompatible-Replacement-MFC-L2750DW-HL-L2370DWXL-MFC-L2750DWXL%2Fdp%2FB07QMVKX99%2Fref%3Dsr_1_252_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550211%26sr%3D8-252-spons%26psc%3D1&amp;qualifier=1575550211&amp;id=3484599039813543&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg6_1?ie=UTF8&amp;adId=A0923228K7E1ZZ4ZX7W8&amp;url=%2FmyCartridge-Compatible-Cartridge-Replacement-Laserjet%2Fdp%2FB078MLSFXM%2Fref%3Dsr_1_241_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550212%26sr%3D8-241-spons%26psc%3D1&amp;qualifier=1575550212&amp;id=7212786882724726&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg6_2?ie=UTF8&amp;adId=A027016924GI6LGZZLIZ9&amp;url=%2FPrint-Save-Repeat-Lexmark-Extra-Remanufactured-Cartridge%2Fdp%2FB00G000356%2Fref%3Dsr_1_242_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550212%26sr%3D8-242-spons%26psc%3D1&amp;qualifier=1575550212&amp;id=7212786882724726&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg6_3?ie=UTF8&amp;adId=A00081291AW4A7RZIB4Q8&amp;url=%2FPrint-Save-Repeat-Lexmark-E260A21A-Remanufactured-Cartridge%2Fdp%2FB008CI9D5U%2Fref%3Dsr_1_243_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550212%26sr%3D8-243-spons%26psc%3D1&amp;qualifier=1575550212&amp;id=7212786882724726&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg6_4?ie=UTF8&amp;adId=A09468471GC0XCCR9GHS1&amp;url=%2FPrint-Save-Repeat-Lexmark-51B1H00-Remanufactured-Cartridge%2Fdp%2FB07BR6V4L6%2Fref%3Dsr_1_244_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550212%26sr%3D8-244-spons%26psc%3D1&amp;qualifier=1575550212&amp;id=7212786882724726&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/Cool-Toner-Compatible-Replacement-78A/dp/B007PKF9U4/ref=sr_1_245?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-245',
    'https://www.amazon.com/LxTek-Cartridge-E310dw-E514dw-E515dn/dp/B07GCCKWJW/ref=sr_1_246?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-246',
    'https://www.amazon.com/TEINO-Compatible-Cartridge-Replacement-Q2612A/dp/B07W82VVZ8/ref=sr_1_247?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-247',
    'https://www.amazon.com/GREENSKY-TN630-TN660-MFC-L2700DW-DCP-L2540DW/dp/B014S6O1LU/ref=sr_1_248?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-248',
    'https://www.amazon.com/Compatible-MFC-7460DN-MFC-7860DW-DCP-7060D-DCP-7065DN/dp/B07D462H36/ref=sr_1_249?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-249',
    'https://www.amazon.com/Compatible-Cartridge-MFC-9970CDW-HL-4150CDN-Etechwork/dp/B07VZBQRR7/ref=sr_1_250?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-250',
    'https://www.amazon.com/LxTek-Compatible-Cartridge-Replacement-Laserjet/dp/B07C9J1V6D/ref=sr_1_251?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-251',
    'https://www.amazon.com/Samsung-MLT-D116S-Pack-Toner-Crtg/dp/B07M5HKSVQ/ref=sr_1_252?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-252',
    'https://www.amazon.com/OkiData-44574701-Toner-Cartridge-Printers/dp/B003TG6T1Q/ref=sr_1_253?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-253',
    'https://www.amazon.com/JARBO-Compatible-Cartridges-Laserjet-MFP-M477FDW/dp/B07S5XHVPD/ref=sr_1_254?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-254',
    'https://www.amazon.com/Uniwork-Compatible-Cartridge-Replacement-Laserjet/dp/B07H6D2W2J/ref=sr_1_255?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-255',
    'https://www.amazon.com/Brother-HL-L2320D-Mono-Laser-Printer/dp/B00LEA5EHO/ref=sr_1_256?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-256',
    'https://www.amazon.com/Hitze-Compatible-Cartridge-Replacement-MFC-7860DW/dp/B07CGT9D65/ref=sr_1_257?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-257',
    'https://www.amazon.com/LxTek-Compatible-593-BBKD-Cartridge-Monochrome/dp/B01BH95FVQ/ref=sr_1_258?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-258',
    'https://www.amazon.com/LxTek-Toner-TN660-HL-L2360DW-MFC-L2740DW/dp/B07DQMVCLF/ref=sr_1_259?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-259',
    'https://www.amazon.com/JARBO-Compatible-Cartridges-SCX-4729FW-SCX-4729FD/dp/B075KK6HSN/ref=sr_1_260?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-260',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg6_1?ie=UTF8&amp;adId=A00963443I5WQNWM50QLA&amp;url=%2FHIINK-Comaptible-Replacement-TN660-HL-L2340DW%2Fdp%2FB00TS2F4T8%2Fref%3Dsr_1_261_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550212%26sr%3D8-261-spons%26psc%3D1&amp;qualifier=1575550212&amp;id=7212786882724726&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg6_2?ie=UTF8&amp;adId=A08715701ZJ4QGFSUNGKE&amp;url=%2FINK-SALE-Compatible-Cartridge-Replacement%2Fdp%2FB06WVHSGCB%2Fref%3Dsr_1_262_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550212%26sr%3D8-262-spons%26psc%3D1&amp;qualifier=1575550212&amp;id=7212786882724726&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg6_3?ie=UTF8&amp;adId=A03153323EG5SLZ508TFS&amp;url=%2FMYTONER-Compatible-Cartridge-Replacement-imageCLASS%2Fdp%2FB07WYYDB15%2Fref%3Dsr_1_263_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550212%26sr%3D8-263-spons%26psc%3D1&amp;qualifier=1575550212&amp;id=7212786882724726&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg6_4?ie=UTF8&amp;adId=A03076412KHFOKQ1E6IHH&amp;url=%2FYoYoInk-Compatible-Cartridge-Replacement-Brother%2Fdp%2FB07BHMZC6J%2Fref%3Dsr_1_264_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550212%26sr%3D8-264-spons%26psc%3D1&amp;qualifier=1575550212&amp;id=7212786882724726&amp;widgetName=sp_mtf',
    'https://www.amazon.com/Limeink-Compatible-Cartridges-Replacement-Magenta/dp/B07C727GDR/ref=sr_1_265?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-265',
    'https://www.amazon.com/Toner-Talk-Dina-Gonor-ebook/dp/B00G3VP730/ref=sr_1_266?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-266',
    'https://www.amazon.com/Samsung-CLT-K504S-CLT-C504S-CLT-M504S-CLT-Y504S/dp/B07VFC5WT2/ref=sr_1_267?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-267',
    'https://www.amazon.com/Z-Ink-Compatible-Cartridge-Replacement/dp/B077RWDN6X/ref=sr_1_268?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-268',
    'https://www.amazon.com/Compatible-Cartridge-Laserjet-P2015dn-M2727nf/dp/B07DCQ14L4/ref=sr_1_269?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-269',
    'https://www.amazon.com/Brother-DCP-8080-HL-5340D-Cartridge-Packaging/dp/B001W3EJYW/ref=sr_1_270?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-270',
    'https://www.amazon.com/HP-CF371AM-Magenta-Cartridges-LaserJet/dp/B00BQTIZY2/ref=sr_1_271?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-271',
    'https://www.amazon.com/Canon-Original-131-Toner-Cartridge/dp/B00BS6WWVA/ref=sr_1_272?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-272',
    'https://www.amazon.com/Samsung-MLT-D111S-Pack-Toner-Crtg/dp/B07M8DJLQ1/ref=sr_1_273?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-273',
    'https://www.amazon.com/TEINO-Compatible-Replacement-48A-Black/dp/B07W1WXGM8/ref=sr_1_274?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-274',
    'https://www.amazon.com/Ink-Replacement-MFC-L8600CDW-MFC-L8850CDW-HL-L8350CDW/dp/B00NAESAJG/ref=sr_1_275?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-275',
    'https://www.amazon.com/Aztech-Compatible-HL-L6200DW-HLL6200DWT-MFCL6800DW/dp/B07F7V2VM3/ref=sr_1_276?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-276',
    'https://www.amazon.com/Toner-Kingdom-Compatible-Cartridge-Replacement/dp/B07L5JPJSX/ref=sr_1_277?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-277',
    'https://www.amazon.com/CMTOP-Compatible-Cartridge-ImageClass-MF4880DW/dp/B07QX2XDSB/ref=sr_1_278?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-278',
    'https://www.amazon.com/Z-Ink-Compatible-Replacement-TN450/dp/B07GCCMG7P/ref=sr_1_279?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-279',
    'https://www.amazon.com/Kingjet-Compatible-Cartridge-Replacement-Laserjet/dp/B07D58J6SM/ref=sr_1_280?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-280',
    'https://www.amazon.com/HP-CF279A-Cartridge-LaserJet-M12wHP/dp/B01LZJ41VJ/ref=sr_1_281?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-281',
    'https://www.amazon.com/Cool-Toner-Compatible-CE278A-Cartridge/dp/B00J49M5ZG/ref=sr_1_282?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-282',
    'https://www.amazon.com/GREENCYCLE-CB435A-Cartridge-Replacement-LaserJet/dp/B017IOKNCA/ref=sr_1_283?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-283',
    'https://www.amazon.com/OfficeWorld-Compatible-Cartridge-Replacement-Enterprise/dp/B07TGSWVC7/ref=sr_1_284?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-284',
    'https://www.amazon.com/Uniwork-Compatible-Cartridge-Replacement-LBP622Cdw/dp/B07R8SZ1Y8/ref=sr_1_285?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-285',
    'https://www.amazon.com/Brother-TN433BK-TN433C-Magenta-Cartridge/dp/B077512VK7/ref=sr_1_286?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-286',
    'https://www.amazon.com/INK-SALE-Replacement-MFC-L2700DW-DCP-L2540DW/dp/B00OT7BATA/ref=sr_1_287?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-287',
    'https://www.amazon.com/HP-CF258X-Toner-Cartridge-Black/dp/B07QZ4Z3X9/ref=sr_1_288?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-288',
    'https://www.amazon.com/Cool-Toner-Compatible-Replacement-410A/dp/B07RW25GN1/ref=sr_1_289?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-289',
    'https://www.amazon.com/Compatible-Cartridge-Replacement-P2055dn-Laserjet/dp/B07RHSD26N/ref=sr_1_290?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-290',
    'https://www.amazon.com/FDC-Toner-Compatible-WorkCentre-Replacement/dp/B01MYPHN3I/ref=sr_1_291?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-291',
    'https://www.amazon.com/Limeink-Compatible-Cartridges-Replacement-1250c/dp/B01FT3FY0I/ref=sr_1_292?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-292',
    'https://www.amazon.com/Uniwork-Compatible-Cartridge-Replacement-Laserjet/dp/B07QJXR8H2/ref=sr_1_293?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-293',
    'https://www.amazon.com/ejet-Compatible-Cartridge-Replacement-LBP612CDW/dp/B07N3B6RKB/ref=sr_1_294?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-294',
    'https://www.amazon.com/Compatible-Toner-Cartridges-Laserjet-M477fdn/dp/B0751917CF/ref=sr_1_295?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-295',
    'https://www.amazon.com/HP-CF380A-Black-Cartridge-LaserJet/dp/B00IGOQW5Y/ref=sr_1_296?keywords=printer+toner&amp;qid=1575550212&amp;sr=8-296',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg6_1?ie=UTF8&amp;adId=A08310111IQFE0FTLX5Y9&amp;url=%2FCompatible-Cartridge-Laserjet-Printer-EasyPrint%2Fdp%2FB07VRLTRB3%2Fref%3Dsr_1_297_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550212%26sr%3D8-297-spons%26psc%3D1&amp;qualifier=1575550212&amp;id=7212786882724726&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg6_2?ie=UTF8&amp;adId=A04068801JNAUBL0HS4NQ&amp;url=%2FmyCartridge-Toner-Replacement-Canon-054%2Fdp%2FB07RL2C6S8%2Fref%3Dsr_1_298_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550212%26sr%3D8-298-spons%26psc%3D1&amp;qualifier=1575550212&amp;id=7212786882724726&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg6_3?ie=UTF8&amp;adId=A00959441EGA9Z3C5W5CL&amp;url=%2FHIINK-Replacement-DCP-L2520DW-DCP-L2540DW-MFC-L2700DW%2Fdp%2FB075VDJWDV%2Fref%3Dsr_1_299_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550212%26sr%3D8-299-spons%26psc%3D1%26smid%3DA3CPBP1O4SV5Q9&amp;qualifier=1575550212&amp;id=7212786882724726&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg6_4?ie=UTF8&amp;adId=A0740779B6RQ6POG416E&amp;url=%2FMYCARTRIDGE-Replacement-Pro-MFP-M203dw%2Fdp%2FB07W3VRQ25%2Fref%3Dsr_1_300_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550212%26sr%3D8-300-spons%26psc%3D1&amp;qualifier=1575550212&amp;id=7212786882724726&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg7_1?ie=UTF8&amp;adId=A0865425JH1FAWC286BY&amp;url=%2FYoYoInk-Compatible-Black-Replacement-Brother%2Fdp%2FB07CV76JWY%2Fref%3Dsr_1_289_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550217%26sr%3D8-289-spons%26psc%3D1&amp;qualifier=1575550216&amp;id=820800959065393&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg7_2?ie=UTF8&amp;adId=A08427882LWAV8UE8GERM&amp;url=%2FNoahArk-Compatible-Cartridge-Replacement-Magenta%2Fdp%2FB074SCGRBC%2Fref%3Dsr_1_290_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550217%26sr%3D8-290-spons%26psc%3D1&amp;qualifier=1575550216&amp;id=820800959065393&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg7_3?ie=UTF8&amp;adId=A036787234YRFT3JU11PF&amp;url=%2FMYTONER-Brother-TN227-HL-L3230CDW-MFC-L3710CW%2Fdp%2FB07SM79JJD%2Fref%3Dsr_1_291_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550217%26sr%3D8-291-spons%26psc%3D1&amp;qualifier=1575550216&amp;id=820800959065393&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_next_aps_sr_pg7_4?ie=UTF8&amp;adId=A025921823UJJ3EJ6DOY4&amp;url=%2FYoYoInk-Compatible-Replacement-Brother-1-Pack%2Fdp%2FB00IS8O2C8%2Fref%3Dsr_1_292_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550217%26sr%3D8-292-spons%26psc%3D1&amp;qualifier=1575550216&amp;id=820800959065393&amp;widgetName=sp_atf_next',
    'https://www.amazon.com/Cartlee-Compatible-Cartridges-Replacement-Printers/dp/B07G8BBCJ2/ref=sr_1_293?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-293',
    'https://www.amazon.com/TN760-Compatible-Brother-HLL2395DW-HLL2350DW/dp/B07FN1DTWF/ref=sr_1_294?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-294',
    'https://www.amazon.com/Arcon-Compatible-Cartridge-Replacement-Laserjet/dp/B07JXZ17YP/ref=sr_1_295?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-295',
    'https://www.amazon.com/Brother-Genuine-Cartridge-TN650-Replacement/dp/B001W36YM2/ref=sr_1_296?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-296',
    'https://www.amazon.com/Brother-TN431M-Standard-Toner-Retail-Packaging/dp/B06XCD5LRB/ref=sr_1_297?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-297',
    'https://www.amazon.com/LINKYO-Compatible-Cartridge-Replacement-CF280A/dp/B073XTDWW7/ref=sr_1_298?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-298',
    'https://www.amazon.com/GREENSKY-Compatible-CLT-K404S-Toner-Replacement/dp/B07JBK4PK9/ref=sr_1_299?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-299',
    'https://www.amazon.com/GTS-Cartridges-SL-M2825DW-SL-M2875FD-SL-M2835DW/dp/B01J92ENZC/ref=sr_1_300?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-300',
    'https://www.amazon.com/Starink-Compatible-Cartridge-Replacement-Laserjet/dp/B07D52PJML/ref=sr_1_301?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-301',
    'https://www.amazon.com/HI-VISION-Compatible-593-BBMF-Cartridge-Replacement/dp/B0163LCUGQ/ref=sr_1_302?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-302',
    'https://www.amazon.com/Z-Ink-Replacement-Samsung-111L/dp/B00MAG0VNI/ref=sr_1_303?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-303',
    'https://www.amazon.com/V4INK-Compatible-Replacement-CF283A-Cartridge/dp/B00I03H78M/ref=sr_1_304?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-304',
    'https://www.amazon.com/Canon-Original-High-Capacity-Cartridge/dp/B00BS6WWTW/ref=sr_1_305?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-305',
    'https://www.amazon.com/HI-VISION-Compatible-MLT-D203L-Cartridge-SL-M3820DW/dp/B00QJDIF18/ref=sr_1_306?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-306',
    'https://www.amazon.com/LD-Compatible-Cartridge-Replacement-CF410X/dp/B01BUCCTC8/ref=sr_1_307?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-307',
    'https://www.amazon.com/Aztech-Compatible-M477fnw-Cartridge-Laserjet/dp/B07CML3BG3/ref=sr_1_308?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-308',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg7_1?ie=UTF8&amp;adId=A06618983CNWIXUEAPDCW&amp;url=%2FStarink-Compatible-Cartridge-Laserjet-Printers%2Fdp%2FB07D5DXLWV%2Fref%3Dsr_1_309_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550217%26sr%3D8-309-spons%26psc%3D1&amp;qualifier=1575550216&amp;id=820800959065393&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg7_2?ie=UTF8&amp;adId=A09347393BW97HPS38GYM&amp;url=%2FBAISINE-Cartridge-Compatible-Laserjet-Enterprise%2Fdp%2FB07L5H17H8%2Fref%3Dsr_1_310_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550217%26sr%3D8-310-spons%26psc%3D1&amp;qualifier=1575550216&amp;id=820800959065393&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg7_3?ie=UTF8&amp;adId=A003697324ZR30NWN5YR8&amp;url=%2FHIINK-Cartridge-Replacement-LaserJet-P2055dn%2Fdp%2FB01B71HNWI%2Fref%3Dsr_1_311_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550217%26sr%3D8-311-spons%26psc%3D1&amp;qualifier=1575550216&amp;id=820800959065393&amp;widgetName=sp_mtf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg7_4?ie=UTF8&amp;adId=A081573930S0KVJON0GIJ&amp;url=%2FLEMERO-Compatible-Cartridge-Replacement-CE285A%2Fdp%2FB07WR44WLH%2Fref%3Dsr_1_312_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550217%26sr%3D8-312-spons%26psc%3D1&amp;qualifier=1575550216&amp;id=820800959065393&amp;widgetName=sp_mtf',
    'https://www.amazon.com/Arcon-Compatible-Replacement-imageCLASS-Printer/dp/B07VSQHB62/ref=sr_1_313?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-313',
    'https://www.amazon.com/HP-Q7553A-Black-Cartridge-LaserJet/dp/B000J6HYL8/ref=sr_1_314?keywords=printer+toner&amp;qid=1575550217&amp;sr=8-314',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg7_1?ie=UTF8&amp;adId=A030779710XOPSU9ZC6ZO&amp;url=%2FYoYoInk-Compatible-Cartridge-Replacement-Brother%2Fdp%2FB07CV7CQ28%2Fref%3Dsr_1_315_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550217%26sr%3D8-315-spons%26psc%3D1&amp;qualifier=1575550216&amp;id=820800959065393&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg7_2?ie=UTF8&amp;adId=A0692675BWXJZ151C0QR&amp;url=%2FYoYoInk-Compatible-Cartridges-Replacement-Brother%2Fdp%2FB07K8J9X4W%2Fref%3Dsr_1_316_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550217%26sr%3D8-316-spons%26psc%3D1&amp;qualifier=1575550216&amp;id=820800959065393&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg7_3?ie=UTF8&amp;adId=A04076683E7AJ6R4U8U6Y&amp;url=%2FShidono-Replacement-DCP-L8410CDW-HL-L8360CDWT-HL-L9310CDWT%2Fdp%2FB07MTBVZFT%2Fref%3Dsr_1_317_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550217%26sr%3D8-317-spons%26psc%3D1&amp;qualifier=1575550216&amp;id=820800959065393&amp;widgetName=sp_btf',
    'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_aps_sr_pg7_4?ie=UTF8&amp;adId=A0533070295IHE527TZ8O&amp;url=%2FBAISINE-Compatible-Cartridge-WorkCentre-Printer%2Fdp%2FB07Q812BDS%2Fref%3Dsr_1_318_sspa%3Fkeywords%3Dprinter%2Btoner%26qid%3D1575550217%26sr%3D8-318-spons%26psc%3D1&amp;qualifier=1575550216&amp;id=820800959065393&amp;widgetName=sp_btf',
]


def process_url(url):
    if 'url=' not in url:
        return url
    return 'https://www.amazon.com' + urllib.unquote(url).split('url=')[1].split('?')[0]


def request_sheet1(url):
    global G_ID

    url = process_url(url)

    html = utils.get_request_html(url, cookie1)

    reg = 'id="productTitle".*?>(.*?)<.*?id="averageCustomerReviews_feature_div"(.*?)id="ask_feature_div"(.*?)primeExclusiveBadge_feature_div'

    if 'id="productTitle"' not in html or 'id="averageCustomerReviews_feature_div"' not in html or 'id="ask_feature_div"' not in html or 'primeExclusiveBadge_feature_div' not in html:
        print G_ID, url, 'skip'
        G_ID += 1
        return
    data_list = re.compile(reg).findall(html)

    if data_list:
        title = utils.remove_html_tag(data_list[0][0]).strip()
        rating, no_rating = get_rating(data_list[0][1])
        question = get_question(data_list[0][2])

        one_row = [G_ID, title, url, rating, no_rating, question]

        sheet1.append(one_row)

        if question != 'N/A':
            l_2 = request_sheet2(G_ID, url, question)
        else:
            sheet2.append([G_ID, url, 'N/A', 'N/A'])
            l_2 = -1

        print one_row, l_2

        G_ID += 1


def get_rating(ori):
    if 'acrCustomerReviewText' in ori and 'a-icon a-icon-star' in ori:
        reg = 'a-icon a-icon-star.*?span.*?>(.*?) .*?id="acrCustomerReviewText".*?>(.*?) '
        return re.compile(reg).findall(ori)[0]
    return 'N/A', 'N/A'


def get_question(ori):
    if 'id="askATFLink"' in ori:
        reg = 'id="askATFLink".*?span.*?>(.*?) an'
        return re.compile(reg).findall(ori)[0].strip().replace(',', '').replace('+', '')
    return 'N/A'


def get_question_url(url):
    id = url.split('/dp/')[-1].split('/')[0]

    return 'https://www.amazon.com/ask/questions/asin/' + id + '/'


def request_sheet2(uid, url, no_q):

    q_url_base = get_question_url(url)

    count = int(no_q) / 10 + 1

    reg = 'vote voteAjax.*?data-count="(.*?)".*?a-col-right.*?data-action="ask-no-op".*?>(.*?)<'

    total_count = 0

    for i in range(1, count+1):
        q_url = q_url_base + str(i)

        html = utils.get_request_html(q_url, cookie1)

        data_list = re.compile(reg).findall(html)
        for data in data_list:
            one_row = [uid, url, data[0], data[1].strip()]
            sheet2.append(one_row)
            total_count += 1
    return total_count


def request_sheet3(uid, url):
    global G_ID
    id = url.split('/dp/')[-1].split('/')[0]

    d_url = 'https://www.amazon.com/hz/reviews-render/ajax/lazy-widgets/stream?&csrf=giJa%2BzNRQeQPOoQFx62%2B0jgitgPZsKqftt%2F3yFwAAAABAAAAAF3n7tFyYXcAAAAA%2B4kUEk%2F7iMGR3xPcX6iU&lazyWidget=cr-summarization-attributes&lazyWidget=cr-skyfall&lazyWidget=cr-solicitation&lazyWidget=cr-summarization-lighthut&asin=' + id

    html = utils.post_request_html(d_url, cookie1)

    reg = 'lighthouseTerms.*?:\\\\"(.*?)\\\\"'

    data = re.compile(reg).findall(html)


    if data:
        items = data[0].split('/')
        for item in items:
            one_row = [uid, url, item]
            sheet3.append(one_row)
        return len(items)

    else:
        sheet3.append([uid, url, 'N/A'])
        return -1


def read_excel(filename, start=1):
    global alldata
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    for i in range(start, table.nrows):
        url = table.row(i)[4].value
        g_id = table.row(i)[0].value
        if g_id not in ['AM_140']:
            continue
        try:
            request_sheet2(g_id, url)
        except Exception as e:
            print 'read excel exception--', e, g_id
        time.sleep(2)


def request_urls(url):
    html = utils.get_request_html(url, cookie1)
    utils.write_html(html, '0.html')
    reg = 'a-link-normal a-text-normal.*?href="(.*?)"'

    items = re.compile(reg).findall(html)

    for item in items:
        print 'https://www.amazon.com' + item


def get_sheet0():
    url_base = 'https://www.amazon.com/s?k=printer+toner&page='
    for i in range(1, 8):
        request_urls(url_base + str(i))


# request_sheet1('https://www.amazon.com/Fine-Art-Printing-Photographers-Exhibition/dp/1937538249/ref=sr_1_106?keywords=printer+ink&amp;qid=1575476862&amp;sr=8-106')

def get_sheet1_2():
    for url in urls:
        request_sheet1(url)
    utils.write_excel('sheet1.xls', sheet1)
    utils.write_excel('sheet2.xls', sheet2)


def get_sheet3():
    for i in range(len(urls)):
        print urls[i], request_sheet3(i+1, urls[i])
    utils.write_excel('sheet3.xls', sheet3)


get_sheet1_2()
