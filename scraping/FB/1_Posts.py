# coding: utf-8
import sys, urllib
import urllib2
import re
import HTMLParser
import time, datetime
import xlwt
import os
import httplib

'''
data format:
https://www.facebook.com/pages_reaction_units/more/
?page_id=119197964825456
&cursor={"timeline_cursor":
    "timeline_unit:1:00000000001465461907:04611686018427387904:09223372036854775800:04611686018427387904",
    "timeline_section_cursor":{},
    "has_next_page":true
}
&surface=www_pages_home&unit_count=8&dpr=2
&__user=0&__a=1&__dyn=7xeXxaER0gbgmwCwRAKGzEy4--C11xG3Kq5Qbxu13wmeexZ3orxuE98KaxeUdUlDixa2qnDBxe6o8fypUlxq2K2S1typ9Uqx24o&__req=5&__be=0&__pc=PHASED:DEFAULT&__rev=2385596
https://www.facebook.com/pages_reaction_units/more/
?page_id=123614990983436
&cursor={"timeline_cursor":
    "timeline_unit:1:00000000001523851389:04611686018427387904:09223372036854775800:04611686018427387904",
    "timeline_section_cursor":{},
    "has_next_page":true}
&surface=www_pages_home&unit_count=8&dpr=2
&__user=100006957738125&__a=1&__dyn=5V4cjLx2ByK5A9UkKHqAyqomzFEbEyGgS8VpQAjFGA6EvxuES2N6xvyEybGqK6qxeqaxu9wwz8KFUKbnyogyEnGi4FpeuUuF3e2e5WDokzUhyKdyU8rh4jUXVubx11rDAyF8O49ElwQUlByECQi8yFUix6cw_xrUtVe49888vGfCCgWrxjyoG69Q4UlDBgS6p8szoGqfxmfCx6WLBx6695UCUZqBxeybaWzQQ25iK8wDAyXCAzUx39rgCdUcUpx3yUymf-KeAKqUS4oCiEWbAzecUyma-KaDU8fl4yFppbhe4S2eh4yESQ9BK4pUV1bCxe9yEgxO5oggSGDz8uz8JyV8&__req=18&__be=1&__pc=PHASED:DEFAULT&__rev=3882616&__spin_r=3882616&__spin_b=trunk&__spin_t=1525609587
'''

stop = False
last_time = 0
urls = [
    ["https://www.facebook.com/cocobongoshow/", "CocoBongo", "", ""],
    ["https://www.facebook.com/COPA-RUMBA-124733624250777/", "COPA RUMBA", "", ""],
    ["https://www.facebook.com/CuervosAntroBanda.mx/", "Cuervos Antro Banda", "", ""],
    ["https://www.facebook.com/ElAlegreCuu/", "El Alegre", "", ""],
    ["https://www.facebook.com/ElOlvidoBandaBar/", "El Olvido", "", ""],
    ["https://www.facebook.com/evolutiondiscotequejrz/", "Evolution Discoteque", "", ""],
    ["https://www.facebook.com/Mambocafe.elnuevoritmo/", "Mambocafé - Insurgentes", "", ""],
    ["https://www.facebook.com/destileriasinrival/", "MARTINA LEON OFICIAL", "", ""],
    ["https://www.facebook.com/ovejanegrarevo/", "Oveja Live", "", ""],
    ["https://www.facebook.com/REDXSNIGHTCLUB/", "RED XS", "", ""],
    ["https://www.facebook.com/ReginaClubSocial/", "Regina Club Social", "", ""],
    ["https://www.facebook.com/TequilaAntroBanda/", "Tequila Antro Banda", "", ""],
    ["https://www.facebook.com/TheCityCancun/", "The City Cancun", "", ""],
    ["https://www.facebook.com/thebeatpartyhousee/", "TRIBÚ Bar & Snacks", "", ""],
    ["https://www.facebook.com/XS-PUEBLA-100885659966717/", "XS PUEBLA", "", ""],
    ["https://www.facebook.com/ChambelanesArlequin/", "Chambelanes Arlequín", "", ""],
    ["https://www.facebook.com/MySiluetGdl/", "Spa My Siluet Gdl", "", ""],
    ["https://www.facebook.com/DelSolMexico/", "DelSol", "", ""],
    ["https://www.facebook.com/hemsaladelborreguito/", "Hemsa", "", ""],
    ["https://www.facebook.com/moda.suburbia/", "Suburbia", "", ""],
    ["https://www.facebook.com/TrenBeZapatos/", "Be Trendy Guadalajara", "", ""],
    ["https://www.facebook.com/converse/", "CONVERSE", "", ""],
    ["https://www.facebook.com/falconidonas1/", "Falconi donas", "", ""],
    ["https://www.facebook.com/keikfondant/", "Kéik Fondant Pasteleria", "", ""],
    ["https://www.facebook.com/lapostrerialpz/", "La Postrería BCS", "", ""],
    ["https://www.facebook.com/lluviadeazucarmx/", "Lluvia de Azucar", "", ""],
    ["https://www.facebook.com/PasteleriaLosCedros/", "Pastelería Los Cedros", "", ""],
    ["https://www.facebook.com/suspirospastelerias.franquicias/", "Suspiros Pastelerias", "", ""],
    ["https://www.facebook.com/terecazolamx/", "Tere Cazola", "", ""],
    ["https://www.facebook.com/WingsExpressBCS/", "Wings Express La Paz", "", ""],
    ["https://www.facebook.com/cantinalasanta/", "Cantina Quita Penas La Santa", "", ""],
    ["https://www.facebook.com/AcaLasDonas/", "TiaJuana DONUT BAR", "", ""],
    ["https://www.facebook.com/comienzosanovidasanamx/", "Comienzo Sano Vida Sana MX", "", ""],
    ["https://www.facebook.com/baepagee/", "B a e.", "", ""],
    ["https://www.facebook.com/conexionpueblacom/", "ConexionPuebla.Com", "", ""],
    ["https://www.facebook.com/conociendomxoficial/", "Conociendo México", "", ""],
    ["https://www.facebook.com/SoyElPoblano/", "El Poblano", "", ""],
    ["https://www.facebook.com/FiestasDeOctubreJal/", "Fiestas de Octubre", "", ""],
    ["https://www.facebook.com/heladooscuropy/", "Helado Oscuro", "", ""],
    ["https://www.facebook.com/LasKardashianEnCuliacan/", "Las Kardashian en Culiacán", "", ""],
    ["https://www.facebook.com/NotiShore/", "Noti Shore", "", ""],
    ["https://www.facebook.com/Team.Pictures.of.Tumblr.OFICIAL/", "Pictures of Tumblr", "", ""],
    ["https://www.facebook.com/SiSoyMamonaOficial/", "Sí, Soy Mamona.", "", ""],
    ["https://www.facebook.com/tijuanaeventos/", "Tijuana Eventos", "", ""],
    ["https://www.facebook.com/tijlocal/", "Tijuana Local", "", ""],
    ["https://www.facebook.com/TIJUANAD4S/", "TIJUANADAS", "", ""],
    ["https://www.facebook.com/tkm/", "TKM", "", ""],
    ["https://www.facebook.com/Todo-para-fiestas-Tj-402748849743153/", "Todo para fiestas Tj", "", ""],
    ["https://www.facebook.com/VIXGlamEs/", "VIX Glam Español", "", ""],
    ["https://www.facebook.com/el.paraiso.wonderland/", "W o n d e r l α n d", "", ""],
    ["https://www.facebook.com/pfundidora/", "Parque Fundidora", "", ""],
    ["https://www.facebook.com/ZooParqueLoroPuebla/", "Zoo Parque Loro Puebla", "", ""],
    ["https://www.facebook.com/Quinta-Victoria-511910578859912/", "Quinta Victoria", "", ""],
    ["https://www.facebook.com/cygpoliforum/", "Agenda Guanajuato", "", ""],
    ["https://www.facebook.com/FiestaJuarezEnFamilia/", "Fiesta Juárez", "", ""],
    ["https://www.facebook.com/GranFeriaRegia/", "Gran Feria Regia", "", ""],
    ["https://www.facebook.com/elcabuss/", "El Cabus Burguers", "", ""],
    ["https://www.facebook.com/RockettoRockMyFood/", "Rocketto", "", ""],
    ["https://www.facebook.com/WingStopMex/", "Wingstop México", "", ""],
    ["https://www.facebook.com/amoremiojoyeria/", "Amore Mio", "", ""],
    ["https://www.facebook.com/dairyqueen/", "Dairy Queen", "", ""],
    ["https://www.facebook.com/Eloteriachih/", "Eloteria", "", ""],
    ["https://www.facebook.com/vaquerasfastfood/", "Las Vaqueras", "", ""],
    ["https://www.facebook.com/MayamiWings/", "Mayami WINGS", "", ""],
    ["https://www.facebook.com/McDonalds/", "McDonald's", "", ""],
    ["https://www.facebook.com/shugu.mx/", "SHUGU", "", ""],
    ["https://www.facebook.com/SirloinBuffetBC/", "Sirloin Buffet Baja", "", ""],
    ["https://www.facebook.com/holidanceofcolours/", "Holi Dance of Colours", "", ""],
    ["https://www.facebook.com/luztopia/", "Luztopía", "", ""],
    ["https://www.facebook.com/MachacaFestival/", "Machaca", "", ""],
    ["https://www.facebook.com/PalNorteOficial/", "Tecate Pal Norte", "", ""],
    ["https://www.facebook.com/Cawnas/", "Cawnas", "", ""],
    ["https://www.facebook.com/LaMarujaNice/", "La Maru", "", ""],
    ["https://www.facebook.com/PerraRuin/", "PerraRuin", "", ""],
    ["https://www.facebook.com/PoliciasCancunOficial/", "Policías Cancún", "", ""],
    ["https://www.facebook.com/Siclaroweb/", "Si Claro", "", ""],
    ["https://www.facebook.com/DespicableMe/", "Despicable Me", "", ""],
    ["https://www.facebook.com/TheHungerGamesMovie/", "The Hunger Games", "", ""],
    ["https://www.facebook.com/minions/", "Minions", "", ""],
    ["https://www.facebook.com/applebeesmexico/", "Applebee's México", "", ""],
    ["https://www.facebook.com/BonafontMX/", "Bonafont", "", ""],
    ["https://www.facebook.com/CervezaEstrella/", "Cerveza Estrella", "", ""],
    ["https://www.facebook.com/CrunchMexico/", "Crunch México", "", ""],
    ["https://www.facebook.com/DeliciasDelContry/", "Delicias Del Contry", "", ""],
    ["https://www.facebook.com/fantapakistan/", "Fanta", "", ""],
    ["https://www.facebook.com/Frisosingapore/", "Friso Singapore", "", ""],
    ["https://www.facebook.com/GranvitaMx/", "Granvita", "", ""],
    ["https://www.facebook.com/heladosultana/", "Helados Sultana", "", ""],
    ["https://www.facebook.com/LaVillitaMX/", "La Villita", "", ""],
    ["https://www.facebook.com/lyncott/", "Lyncott", "", ""],
    ["https://www.facebook.com/mamutmamutmx/", "Mamut", "", ""],
    ["https://www.facebook.com/mrpaypasteleria/", "Mr. Pay Pastelerias", "", ""],
    ["https://www.facebook.com/philadelphiamx/", "Queso Philadelphia México", "", ""],
    ["https://www.facebook.com/QuesosNocheBuena/", "Quesos NocheBuena", "", ""],
    ["https://www.facebook.com/spriteus/", "Sprite", "", ""],
    ["https://www.facebook.com/StarbucksMexico/", "Starbucks Mexico", "", ""],
    ["https://www.facebook.com/supermercadossmart/", "Supermercados S-Mart", "", ""],
    ["https://www.facebook.com/zitlayzicatelamx/", "Zitla y Zicatela México", "", ""],
    ["https://www.facebook.com/desayunospersonalizadosencancun/", "Desayunos Personalizados en Cancun", "", ""],
    ["https://www.facebook.com/LokoFactory/", "Loko Factory", "", ""],
    ["https://www.facebook.com/arreglosfrutalescancun/", "Arreglos Frutales Cancún", "", ""],
    ["https://www.facebook.com/envialeglobos/", "Envialeglobos.com", "", ""],
    ["https://www.facebook.com/Faranushh/", "Faranush", "", ""],
    ["https://www.facebook.com/SweetGiftMX/", "Sweet-Gift", "", ""],
    ["https://www.facebook.com/agimnasia/", "AGimnasia Tijuana", "", ""],
    ["https://www.facebook.com/californiafitnessmexico/", "California Fitness", "", ""],
    ["https://www.facebook.com/Extenciones-Michelita-cabello-100-natural-1620136664939971/", "Extenciones Michelita cabello 100% natural", "", ""],
    ["https://www.facebook.com/helwesalon/", "Helwe - Hair & Makeup Artists", "", ""],
    ["https://www.facebook.com/MilanezHairStudio/", "Milanez hair studio", "", ""],
    ["https://www.facebook.com/nancygarher/", "Peiname", "", ""],
    ["https://www.facebook.com/Style-your-Hair-806265156081572/", "Style your Hair", "", ""],
    ["https://www.facebook.com/centrosaludybellezaspa/", "Centro Integral Salud y Belleza", "", ""],
    ["https://www.facebook.com/CAPELI.hairtools/", "Capeli", "", ""],
    ["https://www.facebook.com/Elizabeth-Gonzalez-830008483719149/", "Elizabeth Gonzalez", "", ""],
    ["https://www.facebook.com/eos/", "eos", "", ""],
    ["https://www.facebook.com/Instituto-Mona-Professional-Makeup-618900151560869/", "Instituto Mona Professional Makeup", "", ""],
    ["https://www.facebook.com/KotexMexico/", "Kotex México", "", ""],
    ["https://www.facebook.com/lorealparisindia/", "L'Oréal Paris", "", ""],
    ["https://www.facebook.com/marykaydemexico/", "Mary Kay de México", "", ""],
    ["https://www.facebook.com/naturabrasil.us/", "NaturaBrasil US", "", ""],
    ["https://www.facebook.com/odontoespecializadachih/", "ODONTOLOGIA ESPECIALIZADA", "", ""],
    ["https://www.facebook.com/PanteneIndia/", "Pantene India", "", ""],
    ["https://www.facebook.com/Velvet-Cosmetics-142437406183389/", "Velvet Cosmetics", "", ""],
    ["https://www.facebook.com/uacjmx/", "Universidad Autónoma de Ciudad Juárez", "", ""],
    ["https://www.facebook.com/SoyTaniaRin/", "Tania Rincón", "", ""],
    ["https://www.facebook.com/dekorcentermx/", "Dekor Center", "", ""],
    ["https://www.facebook.com/dairyqueen/", "Dairy Queen", "", ""],
    ["https://www.facebook.com/OfficialHeladosTrevly/", "Helados Trevly", "", ""],
    ["https://www.facebook.com/lemimehelados/", "Le Mime - Helados en Rollo", "", ""],
    ["https://www.facebook.com/CapriccioPizzaPasta/", "Capriccio Pizza & Pasta", "", ""],
    ["https://www.facebook.com/francachelamx/", "Francachela Pizzería", "", ""],
    ["https://www.facebook.com/azuljoyascancun/", "Azul Cancún", "", ""],
    ["https://www.facebook.com/emperijoyada/", "Emperijoyada Mayoreo", "", ""],
    ["https://www.facebook.com/anhelomx/", "Anhelo", "", ""],
    ["https://www.facebook.com/Etcétera-Accesorios-364141408975/", "Etcétera Accesorios", "", ""],
    ["https://www.facebook.com/Joyería-y-Relojería-El-tiempo-es-Oro-314572499349884/", "Joyería y Relojería El tiempo es Oro", "", ""],
    ["https://www.facebook.com/Silhouette28/", "Silhouette 28", "", ""],
    ["https://www.facebook.com/AcabateloMTY/", "Acábatelo MTY", "", ""],
    ["https://www.facebook.com/cosasbuchonas/", "COSAS BUCHONAS", "", ""],
    ["https://www.facebook.com/iCosasDeNovios/", "Cosas de Novios", "", ""],
    ["https://www.facebook.com/DesmadreYuca/", "Desmadre Yucateco.", "", ""],
    ["https://www.facebook.com/erinfinitos/", "Éramos Infinitos.", "", ""],
    ["https://www.facebook.com/Parkflytrampoline/", "Fly Trampoline Park", "", ""],
    ["https://www.facebook.com/halloweenenelzoo/", "Halloween en el Zoo", "", ""],
    ["https://www.facebook.com/HorrorFestMty/", "HORROR FEST MONTERREY", "", ""],
    ["https://www.facebook.com/JuanDeDiosPantojaCorona/", "Juan De Dios Pantoja Corona", "", ""],
    ["https://www.facebook.com/mehpushiLaPaz/", "Meh pushi La Paz", "", ""],
    ["https://www.facebook.com/memescancunoficial/", "Memes Cancún", "", ""],
    ["https://www.facebook.com/mujerescabronasy/", "Mujeres cabronas y mas", "", ""],
    ["https://www.facebook.com/nuevoleonesunico/", "Nuevo León Es Único", "", ""],
    ["https://www.facebook.com/NuevoLeonymas1/", "NUEVO LEÓN y más", "", ""],
    ["https://www.facebook.com/Puro-desmadre-BCS-849011005204271/", "Puro desmadre BCS", "", ""],
    ["https://www.facebook.com/skyzonetijuana/", "Sky Zone Tijuana", "", ""],
    ["https://www.facebook.com/viralAmericaa/", "Troll BCS 1", "", ""],
    ["https://www.facebook.com/WhatsSad-1509281909083859/", "WhatsSad", "", ""],
    ["https://www.facebook.com/AuditorioTELMEX/", "Auditorio TELMEX", "", ""],
    ["https://www.facebook.com/TeatroDiana/", "Teatro Diana", "", ""],
    ["https://www.facebook.com/Elviajerofisgon/", "El Viajero Fisgón", "", ""],
    ["https://www.facebook.com/GuanajuatoMexico/", "Estado de Guanajuato, México", "", ""],
    ["https://www.facebook.com/GtoMeConquista/", "Guanajuato Me Conquista.", "", ""],
    ["https://www.facebook.com/PueblaTravel/", "Puebla.Travel", "", ""],
    ["https://www.facebook.com/vivalapaz/", "Viva La Paz", "", ""],
    ["https://www.facebook.com/REVISTAPORTI/", "Por Ti de J-14", "", ""],
    ["https://www.facebook.com/triangulo700/", "Revista Triangulo Politico", "", ""],
    ["https://www.facebook.com/avivanailandhair/", "AVIVA Hair & Makeup Salon", "", ""],
    ["https://www.facebook.com/Cassandra-Cassou-Makeup-Studio-693501307455152/", "Cassandra Cassou Makeup Studio", "", ""],
    ["https://www.facebook.com/DulceVegaMakeupArtistStudio/", "DULCE VEGA makeup artist studio", "", ""],
    ["https://www.facebook.com/claseyestilomx/", "ESCUELA CLASE Y ESTILO", "", ""],
    ["https://www.facebook.com/saraelymaldonado/", "Sara Maldonado Trujillo", "", ""],
    ["https://www.facebook.com/studiosmakeup/", "Studio S Makeup", "", ""],
    ["https://www.facebook.com/MoldeArte/", "MoldeArte", "", ""],
    ["https://www.facebook.com/ComedorUrbano/", "Comedor Urbano", "", ""],
    ["https://www.facebook.com/Hacienda-el-paraíso-1680027392278194/", "Hacienda el paraíso", "", ""],
    ["https://www.facebook.com/latortaplaza/", "La Torta Plaza", "", ""],
    ["https://www.facebook.com/RestauranteLosMagueyesLaPaz/", "Los Magueyes La Paz", "", ""],
    ["https://www.facebook.com/marakamecafe/", "Marakame Café Cancún", "", ""],
    ["https://www.facebook.com/tacosperronesbcs/", "Tacos Perrones", "", ""],
    ["https://www.facebook.com/UTOPIA-MODELS-136509409770279/", "UTOPIA MODELS", "", ""],
    ["https://www.facebook.com/panteonrococo/", "Panteon Rococo", "", ""],
    ["https://www.facebook.com/festivalvivelatino/", "Vive Latino", "", ""],
    ["https://www.facebook.com/porquemeencantalacumbia/", "Me Encanta la Cumbia", "", ""],
    ["https://www.facebook.com/AlexisChairesOficial/", "Alexis Chaires", "", ""],
    ["https://www.facebook.com/AlfredoOlivasMusica/", "Alfredo Olivas Oficial", "", ""],
    ["https://www.facebook.com/AltaConsigna/", "Alta Consigna", "", ""],
    ["https://www.facebook.com/arielcamachooficial/", "Ariel Camacho y Los Plebes del Rancho", "", ""],
    ["https://www.facebook.com/AtlGarzaOficial/", "ATL", "", ""],
    ["https://www.facebook.com/BandaCarnavalOfficial/", "Banda Carnaval Oficial", "", ""],
    ["https://www.facebook.com/BandaTrakalosa1/", "Banda La Trakalosa de Monterrey", "", ""],
    ["https://www.facebook.com/LaBandonononaRanchoViejo/", "Banda Rancho Viejo", "", ""],
    ["https://www.facebook.com/CKanMEX/", "C-Kan", "", ""],
    ["https://www.facebook.com/CD9/", "CD9", "", ""],
    ["https://www.facebook.com/hermanossiqueiros/", "Chicarelatable", "", ""],
    ["https://www.facebook.com/chihuasZone/", "ChihuasZone", "", ""],
    ["https://www.facebook.com/yochuylizarraga/", "Chuy Lizarraga", "", ""],
    ["https://www.facebook.com/DivasParranderasYParranderos/", "DivasParranderasYParranderos", "", ""],
    ["https://www.facebook.com/edwinlunat/", "Edwin Luna", "", ""],
    ["https://www.facebook.com/elbebeto.com.mx/", "El Bebeto", "", ""],
    ["https://www.facebook.com/enigmanorteno/", "Enigma Norteno", "", ""],
    ["https://www.facebook.com/GermanMonteroMusica/", "German Montero", "", ""],
    ["https://www.facebook.com/jaryoficial/", "Jary", "", ""],
    ["https://www.facebook.com/javierrosasap/", "Javier Rosas", "", ""],
    ["https://www.facebook.com/KRKevinRoldan/", "KevinRoldan", "", ""],
    ["https://www.facebook.com/adictivaoficial/", "La Adictiva", "", ""],
    ["https://www.facebook.com/poderosasanjuanoficial/", "La Poderosa Banda San Juan", "", ""],
    ["https://www.facebook.com/LaZendaNortena/", "La Zenda Norteña", "", ""],
    ["https://www.facebook.com/LaylOficial/", "Layl", "", ""],
    ["https://www.facebook.com/PrimosMX/", "Los Primos Mx", "", ""],
    ["https://www.facebook.com/luiscoronelmusic/", "Luis Coronel", "", ""],
    ["https://www.facebook.com/lajosaloyola/", "MARIAJOSE", "", ""],
    ["https://www.facebook.com/mcdavoo/", "MCDAVO", "", ""],
    ["https://www.facebook.com/NetoBernalOficial/", "Neto Bernal", "", ""],
    ["https://www.facebook.com/neztormvloficial/", "Neztor MVL", "", ""],
    ["https://www.facebook.com/soypatycantu/", "Paty Cantú", "", ""],
    ["https://www.facebook.com/ReguloCaroNet/", "Regulo Caro", "", ""],
    ["https://www.facebook.com/RemmyValenzuela/", "Remmy Valenzuela", "", ""],
    ["https://www.facebook.com/Revolver-Cannabis-158471010917717/", "Revolver Cannabis", "", ""],
    ["https://www.facebook.com/Santa.RM.Official/", "Santa RM", "", ""],
    ["https://www.facebook.com/sargentorapfetemastudio/", "Sargentorap", "", ""],
    ["https://www.facebook.com/sauleljaguar/", "Saul el jaguar", "", ""],
    ["https://www.facebook.com/UlicesChaidez1/", "Ulices Chaidez", "", ""],
    ["https://www.facebook.com/XimenaMusic/", "Ximena Sariñana", "", ""],
    ["https://www.facebook.com/isabel.flores.96780/", "Andy Nail's Studio", "", ""],
    ["https://www.facebook.com/palafoxsalon/", "Palafox Salon", "", ""],
    ["https://www.facebook.com/VsnaiilsSalon/", "Vs Nails Pedicure Manicure", "", ""],
    ["https://www.facebook.com/wingsarmychihuahua/", "Wings Army Chihuahua", "", ""],
    ["https://www.facebook.com/Alejandro-Patrón-El-Reportero-Urbano-843404809110276/", "Alejandro Patrón / El Reportero Urbano", "", ""],
    ["https://www.facebook.com/aquiesleon/", "Aquí es León", "", ""],
    ["https://www.facebook.com/Bichiware/", "Bichíware", "", ""],
    ["https://www.facebook.com/NoticiasBlancoyNegro/", "Blanco y Negro", "", ""],
    ["https://www.facebook.com/CabronicientaOficial1/", "Cabronicienta", "", ""],
    ["https://www.facebook.com/Centro.Noticias.Tehuacan/", "Centro Noticias Tehuacán", "", ""],
    ["https://www.facebook.com/ChihuahuaDigital/", "Chihuahua Digital", "", ""],
    ["https://www.facebook.com/ChilangoOficial/", "Chilango", "", ""],
    ["https://www.facebook.com/ConciertosGuadalajara/", "Conciertos Guadalajara", "", ""],
    ["https://www.facebook.com/PuntualPuebla/", "Diario Puntual", "", ""],
    ["https://www.facebook.com/EntreLineasNews/", "Entre Líneas", "", ""],
    ["https://www.facebook.com/fisgonpoliticojalisco/", "Fisgón Político", "", ""],
    ["https://www.facebook.com/Frontera.info/", "Frontera.info", "", ""],
    ["https://www.facebook.com/NoticieroGuardiaNocturna/", "Guardia Nocturna", "", ""],
    ["https://www.facebook.com/Jalisco-Rojo-547204055459680/", "Jalisco Rojo", "", ""],
    ["https://www.facebook.com/ZmgJalisco/", "Jalisco ZMG", "", ""],
    ["https://www.facebook.com/laopcion/", "La Opción de Chihuahua", "", ""],
    ["https://www.facebook.com/NBCSnoticias/", "NBCS Noticias", "", ""],
    ["https://www.facebook.com/NoticaribePeninsular/", "Noticaribe", "", ""],
    ["https://www.facebook.com/NoticiasLocalesMx/", "Noticias Locales de Chihuahua", "", ""],
    ["https://www.facebook.com/OCTAVODIAmx/", "OCTAVO DÍA", "", ""],
    ["https://www.facebook.com/PueblaNoticias/", "Puebla Noticias", "", ""],
    ["https://www.facebook.com/QuiuboLeon/", "QuiuboLeón", "", ""],
    ["https://www.facebook.com/notisas/", "Segundo a Segundo", "", ""],
    ["https://www.facebook.com/Soyrayadoytengoaguante/", "Soy rayado y tengo aguante", "", ""],
    ["https://www.facebook.com/traficozmg/", "Trafico Zmg", "", ""],
    ["https://www.facebook.com/tubebeytu/", "Tubebeytu", "", ""],
    ["https://www.facebook.com/UMinutoNoticiasLeon/", "Último Minuto", "", ""],
    ["https://www.facebook.com/uniradioinforma/", "UniradioInforma.com", "", ""],
    ["https://www.facebook.com/yoamotijuanaoficial/", "YO AMO TIJUANA", "", ""],
    ["https://www.facebook.com/yucatan.alminuto/", "Yucatán al Minuto", "", ""],
    ["https://www.facebook.com/Zona-Roja-BCS-1478053342423981/", "Zona Roja BCS", "", ""],
    ["https://www.facebook.com/MOTOREDTEHUACAN/", "Moto Red Tehuacán", "", ""],
    ["https://www.facebook.com/DomingoFelizChihuahua/", "Domingo Feliz Chihuahua", "", ""],
    ["https://www.facebook.com/mundopatitaschihuahua/", "Mundo Patitas Chihuahua", "", ""],
    ["https://www.facebook.com/shlp.ac/", "Sociedad Humanitaria de La Paz", "", ""],
    ["https://www.facebook.com/ParqueChipinque/", "Parque Ecológico Chipinque", "", ""],
    ["https://www.facebook.com/teletonmexicooficial/", "Teletón México", "", ""],
    ["https://www.facebook.com/nutriologavaleriavalencia/", "Nutricion y fitness Vale.", "", ""],
    ["https://www.facebook.com/Coordinación-Estatal-de-Protección-Civil-Quintana-Roo-236425840062787/", "Coordinación Estatal de Protección Civil Quintana Roo", "", ""],
    ["https://www.facebook.com/hersheys/", "HERSHEY'S", "", ""],
    ["https://www.facebook.com/MissTeenagerBeautyMexico/", "Miss Teenager Beauty Mexico", "", ""],
    ["https://www.facebook.com/WOTumblr/", "Tumblr World†", "", ""],
    ["https://www.facebook.com/YosoyLeon.mx/", "YosoyLeón - Gente Positiva", "", ""],
    ["https://www.facebook.com/ArenaMonterreyOficial/", "Arena Monterrey", "", ""],
    ["https://www.facebook.com/AuditorioPabellonM/", "Auditorio Pabellón M", "", ""],
    ["https://www.facebook.com/rancho.sanrafael/", "Curso de Verano Rancho San Rafael", "", ""],
    ["https://www.facebook.com/Domocaremty/", "Domo Care", "", ""],
    ["https://www.facebook.com/FeriaSantaRitaDeChihuahua/", "Feria Santa Rita De Chihuahua", "", ""],
    ["https://www.facebook.com/generalshowcenter/", "GENERAL SHOW CENTER", "", ""],
    ["https://www.facebook.com/PlazaDeLaMeXicanidad/", "Plaza de la MeXicanidad", "", ""],
    ["https://www.facebook.com/FestivaldeNavidad/", "Sueño Magico Festival de Navidad:.", "", ""],
    ["https://www.facebook.com/carteleracdjuarez/", "Cartelera Cd. Juárez", "", ""],
    ["https://www.facebook.com/Tercera-llamada-Chihuahua-1709831352607867/", "Tercera llamada Chihuahua", "", ""],
    ["https://www.facebook.com/Obras-de-teatro-en-Chihuahua-Mitaquillacommx-284117825122114/", "Obras de teatro en Chihuahua & Mitaquilla.com.mx", "", ""],
    ["https://www.facebook.com/Obras-de-teatro-en-Juarez-1434917693486557/", "Obras de teatro en Juarez", "", ""],
    ["https://www.facebook.com/ElClubJF1/", "BBC Club", "", ""],
    ["https://www.facebook.com/PerdidosdeSinaloaOficial/", "Los Perdidos de Sinaloa", "", ""],
    ["https://www.facebook.com/losvendavalesoficial/", "Los Vendavales de Adan Melendez", "", ""],
    ["https://www.facebook.com/YoBailoNortenas/", "Yo Bailo Norteñas_", "", ""],
    ["https://www.facebook.com/ceronueves/", "09.", "", ""],
    ["https://www.facebook.com/i87Oficial/", "87.", "", ""],
    ["https://www.facebook.com/ILoveKarmaPag/", "† K a r m a †", "", ""],
    ["https://www.facebook.com/iSawYourMessage/", "√.", "", ""],
    ["https://www.facebook.com/clubdecochis/", "Club de Cochis", "", ""],
    ["https://www.facebook.com/cosasbienvgas/", "COSAS BIEN VERGAS", "", ""],
    ["https://www.facebook.com/csaspendejasx/", "Cosas pendejas.", "", ""],
    ["https://www.facebook.com/Dejenmellorarcaray/", "Dejenme llorar", "", ""],
    ["https://www.facebook.com/iEdnaModa/", "Edna Moda", "", ""],
    ["https://www.facebook.com/EstoPasaEnLeon/", "Esto Pasa En Leon", "", ""],
    ["https://www.facebook.com/fckpagee/", "Fuck †", "", ""],
    ["https://www.facebook.com/TeamInfiniters/", "Infinity", "", ""],
    ["https://www.facebook.com/lapanzaesprimero1/", "La Panza es Primero", "", ""],
    ["https://www.facebook.com/LaPrincesillaa/", "La Princesilla", "", ""],
    ["https://www.facebook.com/LasPrincesasNoLloranOfi/", "Las Princesas Como Tu No Lloran", "", ""],
    ["https://www.facebook.com/MemesCobachOficial/", "Memes Cobach", "", ""],
    ["https://www.facebook.com/iuhgno/", "No.", "", ""],
    ["https://www.facebook.com/Mundosustentabble/", "Nuevo León Mágico", "", ""],
    ["https://www.facebook.com/tijuanacallesycolonias/", "POR LAS CALLES Y COLONIAS DE TIJUANA", "", ""],
    ["https://www.facebook.com/SadTumbb/", "Sad.", "", ""],
    ["https://www.facebook.com/Situsupierasxna/", "Si tu supieras.", "", ""],
    ["https://www.facebook.com/iSomosPoesia/", "Somos Poesía", "", ""],
    ["https://www.facebook.com/itogetherpagee/", "T o g e t h e r.", "", ""],
    ["https://www.facebook.com/soyrayito/", "Ϟ.", "", ""],
    ["https://www.facebook.com/chuckemexico/", "Chuck E. Cheese's México", "", ""],
    ["https://www.facebook.com/ipchih/", "Incredible Pizza Chihuahua (ipchih)", "", ""],
    ["https://www.facebook.com/LittleCaesars/", "Little Caesars", "", ""],
    ["https://www.facebook.com/misterpizza.esotraonda/", "Mister Pizza", "", ""],
    ["https://www.facebook.com/PeterPiperMexicoOficial/", "Página Oficial de Peter Piper Pizza en México", "", ""],
    ["https://www.facebook.com/pizzaperronegromerida/", "Pizza Del Perro Negro Mérida", "", ""],
    ["https://www.facebook.com/alfonsogonzalezcepeda/", "Mario Alfonso Gonzalez Cepeda", "", ""],
    ["https://www.facebook.com/Las-Micheladas-Camino-Real-363093537230211/", "Las Micheladas Camino Real", "", ""],
    ["https://www.facebook.com/shamrock.juarez/", "Shamrock Juarez", "", ""],
    ["https://www.facebook.com/CerveceriaLaMexicoLaPaz/", "Cervecería La México", "", ""],
    ["https://www.facebook.com/MaleconLaPaz/", "Malecon de La Paz BCS", "", ""],
    ["https://www.facebook.com/Protección-Civil-Cancún-259218067560706/", "Protección Civil Cancún", "", ""],
    ["https://www.facebook.com/AdrianDeLaGarzaS/", "Adrián de la Garza", "", ""],
    ["https://www.facebook.com/AdrianMarceloPrimero/", "Adrian Marcelo Primero", "", ""],
    ["https://www.facebook.com/Aleizzler/", "Aleizzler", "", ""],
    ["https://www.facebook.com/Alexcasasv/", "Alex Casas", "", ""],
    ["https://www.facebook.com/AlexReyesOficial/", "Alex Reyes.", "", ""],
    ["https://www.facebook.com/Strecci/", "AlexXxStrecci", "", ""],
    ["https://www.facebook.com/AntonioEsquincaOficial/", "Antonio Esquinca", "", ""],
    ["https://www.facebook.com/TellezOficial/", "Arely Tellez :)", "", ""],
    ["https://www.facebook.com/OficialVochoAmarillo/", "Bocho Amarillo", "", ""],
    ["https://www.facebook.com/Carlitosfoster1l/", "Carlitos Foster", "", ""],
    ["https://www.facebook.com/CarlossNebot/", "Carlos Nebot", "", ""],
    ["https://www.facebook.com/elcapipe/", "Carlos Perez El Capi", "", ""],
    ["https://www.facebook.com/CosasDePoblanos/", "Cosas De Poblanos", "", ""],
    ["https://www.facebook.com/dhasia.wezka/", "Dhasia Wezka", "", ""],
    ["https://www.facebook.com/djcobramonterrey/", "Dj Cobra Monterrey", "", ""],
    ["https://www.facebook.com/DonAndresOficial/", "Don Andrés", "", ""],
    ["https://www.facebook.com/DonovanMoralesofficial/", "Donovan Morales", "", ""],
    ["https://www.facebook.com/DrLorenzoGonzalezBerchelmann/", "Dr. Lorenzo González Berchelmann", "", ""],
    ["https://www.facebook.com/ElGalloIvan/", "El Gallo Iván Pool", "", ""],
    ["https://www.facebook.com/ElShowDelCachorro/", "El Show Del Cachorro", "", ""],
    ["https://www.facebook.com/ElViejoAmargo/", "El Viejo Amargo", "", ""],
    ["https://www.facebook.com/EraznoYLaChokolata/", "Erazno y la Chokolata", "", ""],
    ["https://www.facebook.com/ernestochavanaoficial/", "Ernesto Chavana", "", ""],
    ["https://www.facebook.com/Marujozz/", "Esau Marujoz", "", ""],
    ["https://www.facebook.com/galatziaoficial/", "Galatzia  Official.", "", ""],
    ["https://www.facebook.com/gisellehernandezofficial/", "Giselle Hernandez", "", ""],
    ["https://www.facebook.com/gregsanchezm/", "Greg Sánchez", "", ""],
    ["https://www.facebook.com/HectorLealVlogs/", "HectorLealVlogs", "", ""],
    ["https://www.facebook.com/irvingtomato/", "Irving Tomato", "", ""],
    ["https://www.facebook.com/Conjdejazmin/", "Jazmín López Villarreal", "", ""],
    ["https://www.facebook.com/JosueBalderramaOfficial/", "Josue Balderrama", "", ""],
    ["https://www.facebook.com/jousinpalafoxnoticias/", "Jousin Palafox Noticias", "", ""],
    ["https://www.facebook.com/juanjaramishow/", "Juan Pablo Jaramillo Estrada", "", ""],
    ["https://www.facebook.com/JuanaHappiness/", "Juana Martinez Hernandez", "", ""],
    ["https://www.facebook.com/ElJuanpaZurita/", "Juanpa Zurita", "", ""],
    ["https://www.facebook.com/Jukilopaa/", "JukiLop", "", ""],
    ["https://www.facebook.com/TeamKaren/", "Karen Polinesia", "", ""],
    ["https://www.facebook.com/kimberlyloaizaa/", "Kimberly Loaiza", "", ""],
    ["https://www.facebook.com/lakonstelacion/", "La Konstelación", "", ""],
    ["https://www.facebook.com/LaMejorTijuana/", "La Mejor Tijuana", "", ""],
    ["https://www.facebook.com/La-niña-bien-1490956914312868/", "La niña bien", "", ""],
    ["https://www.facebook.com/Liz-Elizondo-1625730954349331/", "Liz Elizondo", "", ""],
    ["https://www.facebook.com/LosChicharrines/", "Los Chicharrines", "", ""],
    ["https://www.facebook.com/w2mluisitorey/", "Luisito Rey", "", ""],
    ["https://www.facebook.com/Mario-Andres-Ruiz-449926258397480/", "Mario Andres Ruiz", "", ""],
    ["https://www.facebook.com/MarioBautistaa/", "Mario Bautista", "", ""],
    ["https://www.facebook.com/mirandaibanezface/", "Miranda Ibañez", "", ""],
    ["https://www.facebook.com/Papuoficiall/", "Papu", "", ""],
    ["https://www.facebook.com/elpatozambrano/", "Pato Zambrano", "", ""],
    ["https://www.facebook.com/TeamRaffa/", "Rafa Polinesio", "", ""],
    ["https://www.facebook.com/RafaelMorenoValle/", "Rafael Moreno Valle", "", ""],
    ["https://www.facebook.com/RxlphK/", "Ralph", "", ""],
    ["https://www.facebook.com/Screamau/", "Screamau", "", ""],
    ["https://www.facebook.com/drjuancarlosacosta/", "Sexologo Juan Carlos Acosta", "", ""],
    ["https://www.facebook.com/Silvia-Olmedo-55543311406/", "Silvia Olmedo", "", ""],
    ["https://www.facebook.com/iBelieveInU.BD/", "Taquito †", "", ""],
    ["https://www.facebook.com/textoservidoraa/", "Textoservidora", "", ""],
    ["https://www.facebook.com/TonyGaliFayad/", "Tony Gali Fayad", "", ""],
    ["https://www.facebook.com/ViridianaVelazquezOficial/", "Viridiana Velázquez", "", ""],
    ["https://www.facebook.com/WattSopa/", "Watt Sopa", "", ""],
    ["https://www.facebook.com/yolaconsejera/", "YOLA consejera", "", ""],
    ["https://www.facebook.com/yosstop/", "YosStoP", "", ""],
    ["https://www.facebook.com/RichMusicLT/", "11:11", "", ""],
    ["https://www.facebook.com/magicimagens/", "Memes LPZ", "", ""],
    ["https://www.facebook.com/Anita-Nueva-Aventura-1626561164294552/", "Anita Nueva Aventura", "", ""],
    ["https://www.facebook.com/fiestapark/", "Fiesta Park", "", ""],
    ["https://www.facebook.com/amoramorcafeyreposteria/", "Cafe Amor Amor", "", ""],
    ["https://www.facebook.com/CenasRomanticasGuadalajara/", "Cenas Románticas Guadalajara", "", ""],
    ["https://www.facebook.com/elporfiriatocantina/", "El Porfiriato Paseo La Fe", "", ""],
    ["https://www.facebook.com/Frappemovil/", "Frappemovil La Paz", "", ""],
    ["https://www.facebook.com/latraicionerajuarez5/", "La Traicionera", "", ""],
    ["https://www.facebook.com/LasAlitas/", "Las Alitas", "", ""],
    ["https://www.facebook.com/PaseoChapultepecTijuana/", "Paseo Chapultepec", "", ""],
    ["https://www.facebook.com/okpasteleria/", "Pastelería OK", "", ""],
    ["https://www.facebook.com/Quesabroso-350561685151208/", "Quesabroso", "", ""],
    ["https://www.facebook.com/TheCheesecakeFactoryMexico/", "The Cheesecake Factory México", "", ""],
    ["https://www.facebook.com/Aeropostale/", "Aeropostale", "", ""],
    ["https://www.facebook.com/Forever21/", "Forever 21", "", ""],
    ["https://www.facebook.com/innovasport/", "Innovasport", "", ""],
    ["https://www.facebook.com/CalimaxOficial/", "Calimax", "", ""],
    ["https://www.facebook.com/converse/", "CONVERSE", "", ""],
    ["https://www.facebook.com/EllaDiceCancun/", "Ella Dice", "", ""],
    ["https://www.facebook.com/fisherprice/", "Fisher-Price", "", ""],
    ["https://www.facebook.com/alvaroglobomania/", "Globomania", "", ""],
    ["https://www.facebook.com/Karmen-uñas-y-delineados-permanentes-470245119703586/", "Karmen uñas y delineados permanentes", "", ""],
    ["https://www.facebook.com/LupanaVilchez/", "Lupana Vilchez", "", ""],
    ["https://www.facebook.com/SallyMexico/", "Sally México", "", ""],
    ["https://www.facebook.com/centrocomercialaltacia/", "Centro Comercial Altacia", "", ""],
    ["https://www.facebook.com/fashiondrivemty/", "Fashion Drive", "", ""],
    ["https://www.facebook.com/FashionMallChihuahua/", "Fashion Mall Chihuahua", "", ""],
    ["https://www.facebook.com/GaleriasValleOriente/", "Galerías Valle Oriente", "", ""],
    ["https://www.facebook.com/GPatioZaragoza/", "Gran Patio Zaragoza", "", ""],
    ["https://www.facebook.com/GT.Oblatos/", "Gran Terraza Oblatos", "", ""],
    ["https://www.facebook.com/OutletPuebla.Premiere/", "Outlet Puebla", "", ""],
    ["https://www.facebook.com/Plaza-Andares-Gdl-Jalisco-164427950344385/", "Plaza Andares, Gdl Jalisco", "", ""],
    ["https://www.facebook.com/plazadelasamericascjz/", "Plaza De las Américas", "", ""],
    ["https://www.facebook.com/plazadelsol1969/", "Plaza del Sol Guadalajara", "", ""],
    ["https://www.facebook.com/PlazaDelSur/", "Plaza del Sur", "", ""],
    ["https://www.facebook.com/PlazaGaleriasChihuahua/", "Plaza Galerías Chihuahua", "", ""],
    ["https://www.facebook.com/MKDITO/", "Plaza Mkdito", "", ""],
    ["https://www.facebook.com/plazapaseo2000/", "Plaza Paseo 2000", "", ""],
    ["https://www.facebook.com/PlazaPaseoLaPaz/", "Plaza Paseo La Paz", "", ""],
    ["https://www.facebook.com/plazasenderochihuahua/", "Plaza Sendero Chihuahua", "", ""],
    ["https://www.facebook.com/plazasenderojuarez/", "Plaza Sendero Juarez", "", ""],
    ["https://www.facebook.com/PlazaSenderoLasTorres/", "Plaza Sendero Las Torres", "", ""],
    ["https://www.facebook.com/MarinaTownCenter/", "Puerto Cancun Marina Town Center", "", ""],
    ["https://www.facebook.com/TheShoppesAtLaPaz/", "The Shoppes At La Paz", "", ""],
    ["https://www.facebook.com/CLINICADELACICATRIZ/", "Clínica de la Cicatriz", "", ""],
    ["https://www.facebook.com/KaleSPA/", "Kalé SPA", "", ""],
    ["https://www.facebook.com/lipomedic123/", "Lipomedic", "", ""],
    ["https://www.facebook.com/Skinklinik/", "Skinklinik Med Spa", "", ""],
    ["https://www.facebook.com/ginzacancun/", "GINZA Cancun", "", ""],
    ["https://www.facebook.com/LeyendasDeMonterrey/", "Leyendas de Monterrey", "", ""],
    ["https://www.facebook.com/iTumblrs/", "Tumblr †", "", ""],
    ["https://www.facebook.com/officialsandypage/", "Tumblr †", "", ""],
    ["https://www.facebook.com/SomosDLeon/", "Somos de León", "", ""],
    ["https://www.facebook.com/SoydeTijuana/", "Soy de Tijuana", "", ""],
    ["https://www.facebook.com/SitgesLaPaz/", "Sitges", "", ""],
    ["https://www.facebook.com/AlsuperOficial/", "Alsuper", "", ""],
    ["https://www.facebook.com/lapazaditaindeco/", "La Pazadita Indeco", "", ""],
    ["https://www.facebook.com/institutodebellezaloccoco/", "Instituto Alejandro Loccoco", "", ""],
    ["https://www.facebook.com/discoroller.mx/", "Disco Roller", "", ""],
    ["https://www.facebook.com/AtlasFC/", "Atlas FC", "", ""],
    ["https://www.facebook.com/TorosdeTijuana/", "Toros de Tijuana", "", ""],
    ["https://www.facebook.com/EcoaventurasTrepachanga/", "Ecoaventuras Trepachanga", "", ""],
    ["https://www.facebook.com/TiooGignac/", "El Tío Gignac", "", ""],
    ["https://www.facebook.com/BrassGrillCarneAsada/", "Brass Grill - Carne Asada Y Mariscos.", "", ""],
    ["https://www.facebook.com/SirloinStockadeChihuahua/", "Sirloin Stockade Chihuahua", "", ""],
    ["https://www.facebook.com/ChedrauiQuintanaRoo/", "Chedraui Quintana Roo", "", ""],
    ["https://www.facebook.com/PasteleriaDeLosPobres/", "Pasteleria de los Pobres", "", ""],
    ["https://www.facebook.com/SoloTeriyakiLPZ/", "Solo Teriyaki", "", ""],
    ["https://www.facebook.com/TAJINUSA/", "Tajín", "", ""],
    ["https://www.facebook.com/jirosushi/", "Jiro Sushi", "", ""],
    ["https://www.facebook.com/RSushi1/", "R Sushi", "", ""],
    ["https://www.facebook.com/SUSHILOVELAPAZ/", "Sushi Love", "", ""],
    ["https://www.facebook.com/SushiZoneMexico/", "SUSHI ZONE", "", ""],
    ["https://www.facebook.com/WokSushiSaboresOrientales/", "Wok & Sushi Sabores Orientales", "", ""],
    ["https://www.facebook.com/Blitz-103043446414263/", "Blitz", "", ""],
    ["https://www.facebook.com/Candymaniadulceria/", "Candy Mania Dulceria", "", ""],
    ["https://www.facebook.com/lachucherialapaz/", "La Chuchería", "", ""],
    ["https://www.facebook.com/MEGADULCERIASOTRES/", "MEGA Dulcerias Sotres", "", ""],
    ["https://www.facebook.com/friswim/", "Fri-dasch swimwear", "", ""],
    ["https://www.facebook.com/myselfisthebeachwear/", "Myself Beachwear", "", ""],
    ["https://www.facebook.com/Salon-de-belleza-angel-campos-1183407781753801/", "Salon de belleza angel campos", "", ""],
    ["https://www.facebook.com/buffetcielitolindo/", "Cielito Lindo", "", ""],
    ["https://www.facebook.com/MiCanal5/", "Canal 5", "", ""],
    ["https://www.facebook.com/info7mty/", "info7", "", ""],
    ["https://www.facebook.com/multimediostv/", "Multimedios Televisión", "", ""],
    ["https://www.facebook.com/quierotvGDL/", "OchoTV", "", ""],
    ["https://www.facebook.com/TelevisaGDL/", "Televisa Guadalajara", "", ""],
    ["https://www.facebook.com/TelevisaPuebla/", "Televisa Puebla", "", ""],
    ["https://www.facebook.com/aztecabajio/", "TV Azteca Bajio", "", ""],
    ["https://www.facebook.com/AztecaBCS/", "TV Azteca BCS", "", ""],
    ["https://www.facebook.com/aztecachihuahua/", "TV Azteca Chihuahua", "", ""],
    ["https://www.facebook.com/AztecaCiudadJuarez/", "TV Azteca Ciudad Juárez", "", ""],
    ["https://www.facebook.com/AztecaPueblaOficial/", "TV Azteca Puebla", "", ""],
    ["https://www.facebook.com/tv4guanajuato/", "TV4", "", ""],
    ["https://www.facebook.com/videorolavroficial/", "Video Rola VR", "", ""],
    ["https://www.facebook.com/TelevisaChihuahua/", "Televisa Chihuahua", "", ""],
    ["https://www.facebook.com/Tucanal2tv/", "Tu Canal", "", ""],
    ["https://www.facebook.com/aztecaqroo/", "TV Azteca Quintana Roo", "", ""],
    ["https://www.facebook.com/BuenosDiasJuarezOficial/", "Buenos Dias Juarez", "", ""],
    ["https://www.facebook.com/El-Cafecito-de-la-Mañana-352300878129875/", "El Cafecito de la  Mañana", "", ""],
    ["https://www.facebook.com/EnamorandonosTV/", "Enamorandonos", "", ""],
    ["https://www.facebook.com/ExatlonMx/", "Exatlon Mx", "", ""],
    ["https://www.facebook.com/genteregiaoficial/", "Gente Regia", "", ""],
    ["https://www.facebook.com/LaIslaElReality/", "La Isla el Reality", "", ""],
    ["https://www.facebook.com/lasnoticiastelevisamty/", "Las Noticias Televisa Monterrey", "", ""],
    ["https://www.facebook.com/monterreyaldia/", "Monterrey Al Día", "", ""],
    ["https://www.facebook.com/PlanBAztecaNoreste/", "Plan B Azteca Noreste", "", ""],
    ["https://www.facebook.com/sipsenoticiascancun/", "Sipse Noticias Cancun", "", ""],
    ["https://www.facebook.com/TDJuarez/", "TD Juarez", "", ""],
    ["https://www.facebook.com/vengalaalegria/", "Venga la Alegría", "", ""],
    ["https://www.facebook.com/Mhonivident/", "Mhoni Vidente", "", ""],
    ["https://www.facebook.com/BUAPoficial/", "Benemérita Universidad Autónoma de Puebla - BUAP", "", ""],
    ["https://www.facebook.com/UNAM.MX.Oficial/", "UNAM Universidad Nacional Autónoma de México", "", ""],
    ["https://www.facebook.com/udg.mx/", "Universidad de Guadalajara", "", ""],
    ["https://www.facebook.com/UPAEP/", "UPAEP", "", ""],
    ["https://www.facebook.com/laciteeventos/", "La Cité", "", ""],
    ["https://www.facebook.com/planningbroker/", "Wedding Broker", "", ""],
    ["https://www.facebook.com/6PM-129572671182401/", "6PM", "", ""],
    ["https://www.facebook.com/AguilarBoutique/", "Aguilar Boutique", "", ""],
    ["https://www.facebook.com/JEANSBLUECOLASH/", "BLUE COLASH JEANS", "", ""],
    ["https://www.facebook.com/Boutique-d-Marielos-356557051209962/", "Boutique d Marielos", "", ""],
    ["https://www.facebook.com/BululuBoutique/", "Bululú Boutique", "", ""],
    ["https://www.facebook.com/Camilas-Boutique-532991566822154/", "Camila's Boutique", "", ""],
    ["https://www.facebook.com/carlogiovannivestidos/", "Carlo Giovanni", "", ""],
    ["https://www.facebook.com/carlothadresses/", "Carlotha dresses", "", ""],
    ["https://www.facebook.com/CasaLoveland/", "Casa Loveland", "", ""],
    ["https://www.facebook.com/cherrybluemx/", "Cherry Blue /  Vestidos largos de fiesta", "", ""],
    ["https://www.facebook.com/DevushkaModa/", "Devushka Moda", "", ""],
    ["https://www.facebook.com/rentadevestidosdivinoarmario/", "Divino armario", "", ""],
    ["https://www.facebook.com/duoh.lpz/", "Duoh Clothes", "", ""],
    ["https://www.facebook.com/fabyboutiquelapaz/", "Faby Boutique", "", ""],
    ["https://www.facebook.com/FASHIONCORNERBOU/", "Fashion Corner Boutique", "", ""],
    ["https://www.facebook.com/FashionRoomStoree/", "Fashion Room Store", "", ""],
    ["https://www.facebook.com/fewsha/", "fEWShA", "", ""],
    ["https://www.facebook.com/gamalenceria/", "Gama Lencería", "", ""],
    ["https://www.facebook.com/jokohboutique/", "Jokoh Renta de Vestidos", "", ""],
    ["https://www.facebook.com/Karloz-Zermeño-599905876788690/", "Karloz Zermeño", "", ""],
    ["https://www.facebook.com/kcdresses/", "KC Dresses Renta De Vestidos", "", ""],
    ["https://www.facebook.com/KykDresses/", "Kyk Dresses-Renta de Vestidos", "", ""],
    ["https://www.facebook.com/lacatrinarentadevestidos/", "La Catrina - Renta de Vestidos", "", ""],
    ["https://www.facebook.com/laguerajeansymoda/", "La Güera Jeans & Moda", "", ""],
    ["https://www.facebook.com/LavoroOficial/", "Lavoro", "", ""],
    ["https://www.facebook.com/LittleClosetGdl/", "Little Closet Guadalajara", "", ""],
    ["https://www.facebook.com/ModayEstiloByLittleCloset/", "Little Clóset Moda y Estilo", "", ""],
    ["https://www.facebook.com/Lovelyboutiqueloscabos/", "LovelyBoutique", "", ""],
    ["https://www.facebook.com/MValentinaARshoptiques/", "M. Valentina AR Shoptiques", "", ""],
    ["https://www.facebook.com/matrushkadresses/", "Matrushka Dresses -Renta y Venta de vestidos-", "", ""],
    ["https://www.facebook.com/mazzcancun/", "Mazz", "", ""],
    ["https://www.facebook.com/outfitclothingco/", "OUTFIT Clothing Co", "", ""],
    ["https://www.facebook.com/ozunasrentadevestidos/", "Ozunas renta de vestidos Gómez Morin", "", ""],
    ["https://www.facebook.com/patissboutique/", "Patiss Boutique", "", ""],
    ["https://www.facebook.com/pinkflamingomx/", "PINK FLAMINGO", "", ""],
    ["https://www.facebook.com/queenberrymexico/", "Queenberry Guadalajara", "", ""],
    ["https://www.facebook.com/cancunqc/", "Quinceañeras Cancun", "", ""],
    ["https://www.facebook.com/ReginalShoppe/", "Regina l Shoppe", "", ""],
    ["https://www.facebook.com/Runway.Rentatuvestido/", "Runway Renta de vestidos", "", ""],
    ["https://www.facebook.com/satisfashionmx/", "Satisfashion MX", "", ""],
    ["https://www.facebook.com/SE7VENcuu/", "SE7VEN", "", ""],
    ["https://www.facebook.com/showroomboutiqueregularandplus/", "Showroom Boutique Regular&Plus", "", ""],
    ["https://www.facebook.com/Soholapaz/", "Soho La Paz", "", ""],
    ["https://www.facebook.com/SuaVestidos/", "Súa Designs", "", ""],
    ["https://www.facebook.com/TentacionesCuu/", "Tentaciones", "", ""],
    ["https://www.facebook.com/magnoliasclothing/", "TEZZA", "", ""],
    ["https://www.facebook.com/tutboutique/", "Tut  Fashion Boutique", "", ""],
    ["https://www.facebook.com/valentinos.mx/", "Valentinos", "", ""],
    ["https://www.facebook.com/vestiq/", "Vestiq Renta y Venta de Vestidos", "", ""],
    ["https://www.facebook.com/vogaonline/", "VOGA Boutique", "", ""],
    ["https://www.facebook.com/weeflipflops/", "Wee Flip Flops", "", ""],
    ["https://www.facebook.com/eyca.camacho/", "Yamilet aguilar Ventas Varios", "", ""],
    ["https://www.facebook.com/LaViejonaAgria/", "La Viejona Agria", "", ""],
    ["https://www.facebook.com/xSonrisasFalsas/", "Sonrisas Falsas", "", ""],

]

MAX_PAGE_COUNT = 100
alldata = [['Page Url', 'Page Name', 'No. likes', 'No. follows', 'Post Url', 'Date', 'Main Text', 'No. reactions', 'No. Comment', 'No. Shares', 'No. Views']]
stop_timestamp = 0
start_timestamp = int(time.time())

cookie = 'datr=RKzWW_1NuhIxB9RG7RUemqv0; sb=ovjqW-tww_Qe7OR39cZQ91wp; c_user=100006957738125; xs=145%3Ay4f_mOf19tmvnQ%3A2%3A1542430919%3A20772%3A8703; pl=n; fr=0mVSQPNFOoV7LvCYc.AWURh9sL9hWUa00RS1IrSs2yghE.Bb0aQ1.Cv.FwO.0.0.BcEggY.AWUtWx3-; spin=r.4630630_b.trunk_t.1544685592_s.1_v.2_; wd=1872x422; act=1544685613179%2F1; presence=EDvF3EtimeF1544685613EuserFA21B06957738125A2EstateFDsb2F1516343670424EatF1543282444228Et3F_5b_5dEutc3F1543282444236G544685613825CEchFDp_5f1B06957738125F4CC'
tail = '&surface=www_pages_home&unit_count=8&dpr=2&fb_dtsg_ag=AdyOy3evbM7nAqilKl3HGDrBruy6MaB5MnZViL8daFB0EQ:AdwUt7q2z4S59HmIlCMGzNnpqA5fHxqQZaDLTsjlqldRGg&__user=100006957738125&__a=1&__dyn=7AgNe-4amaUmgDxiWJGi9FxqeCwKyaF3ozGFQAjFGA6EvxGdwIhEnUF7yWCHxCEjCyEgCCG22cyWDyUJoK48G5uF8iBAVXxWAcUeWDUkzWzkaV8ybwxAAhfzLBzoggmVV8Gicx2q5od8nByECVoyaDzp8hz8faxle7-K4bhoeGzVFAeCUgLyo9F44UlDBgS6o8oSaCCy89ooKFprzooAnyrzRGmq9my4aWzXU8l8im2FebKqifyoPKi9zu3e6ogUkGE-WUWiU98ZeEWbAG9UW8Bz9eaDU8fixmmiQhxfyopBzUNqyprypVUV1bCxSaxCbU-2KGDz8uwHh9rADVVHAy8uyUlzF8GWyXwOgigJ5WBDxC8x6GK5EgCy8-pzbzWgK8xicAzE&__req=2d&__be=1&__pc=PHASED:DEFAULT&__rev=4534000&__spin_r=4534000&__spin_b=trunk&__spin_t=1542177655'


def get_ori_html(url):
    page = urllib.urlopen(url)
    html = page.read()
    page.close()
    return html


def write(html, filename):
    fp = open(filename, "w")
    fp.write(html)
    fp.close()
    print "write over"


def remove_html_tag(ori):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', ori)
    return str(HTMLParser.HTMLParser().unescape(dd)).strip()


def get_first_four_column(html, url):
    global last_time
    ''' analysis response to get value of first four columns in excel'''

    global first_four_col, stop
    general_reg = 'class="_5pcr userContentWrapper"(.*?)<form'
    post_list = re.compile(general_reg).findall(html)
    res_photos, res_videos = [], []
    date = ''
    i = None
    for post in post_list:
        if 'photos' in post and 'videos' not in post:
            reg = 'class="_5pcq" href="/(.*?)".*?><abbr title="(.*?)".*?</abbr>.*?<div.*?class=".*?userContent.*?>(.*?)</div>'
            post_detail = re.compile(reg).findall(post)
            if not post_detail:
                continue
            '''i[0] message url; i[1] raw date; i[2] raw message'''
            i = post_detail[0]
            message = remove_html_tag(i[2])
            date = i[1].split(' ')[0]
            message_url = "https://www.facebook.com/" + i[0].split('?')[0]
            res_photos.append([message_url, date, message])
        else:
            reg = 'href="/(.*?)".*?abbr title="(.*?)".*?userContent.*?>(.*?)</div>'
            post_detail = re.compile(reg).findall(post)
            '''i[0] message url; i[1] raw date; i[2] raw message'''
            if not post_detail:
                continue
            i = post_detail[0]
            message = remove_html_tag(i[2])
            date = i[1].split(' ')[0]
            message_url = "https://www.facebook.com/" + i[0]
            res_videos.append([message_url, date, message])
    if not post_list:
        stop = True
        return [], [], 0

    if i:
        try:
            last_time = int(time.mktime(datetime.datetime.strptime(i[1], "%d/%m/%Y, %H:%M").timetuple()))
        except:
            last_time = int(time.mktime(datetime.datetime.strptime(i[1], "%d/%m/%Y %H:%M").timetuple()))
    else:
        last_time -= 500000
    return res_photos, res_videos, last_time


def get_second_four_column(html):
    ''' analysis response to get value of second four columns in excel'''
    second_four_dict = {}
    '''i[0]: post_id, i[1]: comment count; i[2]: like count; i[3]: message URL; i[4]: sharecount'''
    reg = '"canviewerreact":.*?,.*?"commentcount":(.*?),.*?"entidentifier":"(.*?)".*?lc":.*?"likecount":(.*?),.*?"permalink":"(.*?)".*?"sharecount":(.*?),'
    likeshare = re.compile(reg).findall(html)
    for i in likeshare:
        if 'posts' in i[3]:
            photo_link = get_photo_link_of_posts('http://www.facebook.com' + i[3])
            if photo_link:
                key = photo_link.split('/')[-2]
                second_four_dict[key] = [i[2], i[0], i[4]]
        second_four_dict[i[1]] = [i[2], i[0], i[4]]
    return second_four_dict


def scrape_like_follow_of_url(url):
    if '/pages/' in url:
        return
    req = urllib2.Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")
    req.add_header("accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    res = HTMLParser.HTMLParser().unescape(res).decode('unicode-escape').replace('\\', '')
    reg = 'class="_4bl9">(.*?)people like this.*?class="_4bl9".*?>(.*?)people'
    data = re.compile(reg).findall(res)
    return remove_html_tag(data[0][0].split('Page')[1]), remove_html_tag(data[0][1])


def get_photo_link_of_posts(url):
    html = get_request(url)
    reg = 'class="_5pcq" href="(.*?)"'
    res = re.compile(reg).findall(html)
    return res[0] if res else ''


def get_second_four_without_video(html):
    return get_second_four_column(html)


def get_video_view_count(html):
    ''' analysis response to get value of second four columns in excel'''
    second_four_dict = {}
    reg = 'fluentContentToken":"(.*?)".*?"viewCount":"(.*?)"'
    if '"fluentContentToken"' in html and '"viewCount"' in html:
        lists = re.compile(reg).findall(html)
        for i in lists:
            second_four_dict[i[0]] = i[1]
        return second_four_dict
    return {}


def get_req(page_id, time_line, minus8, timestamp):
    '''send response to facebook server to get the return value (6 posts in one time)'''
    '''00000000001531476001:04611686018427387904:09223372036854775803:04611686018427387904'''
    url = "https://www.facebook.com/pages_reaction_units/more/?page_id="

    url += page_id

    data = '&cursor={"timeline_cursor":"timeline_unit:1:0000000000'
    data = data + str(timestamp) + ':' + time_line + ':0' + str(minus8) + ':' + time_line + '",'

    # for now
    data += '"timeline_section_cursor":{},"has_next_page":true}'
    # for 2017
    # data += '"timeline_section_cursor":{"profile_id":' + page_id + ',"start":1514793600,"end":1546329599,"query_type":8,"filter":1,"filter_after_timestamp":1540450373},"has_next_page":true}'
    # for 2018
    # data += '"timeline_section_cursor":{"profile_id":' + page_id + ',"start":0,"end":1543651199,"query_type":36,"filter":1},"has_next_page":true}'
    data += tail
    url += data

    return get_request_of_url(url), url


def get_request_of_url(url):
    print url
    req = urllib2.Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")
    req.add_header("accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    res = HTMLParser.HTMLParser().unescape(res).decode('unicode-escape').replace('\\', '')
    return res


def get_request(url):
    req = urllib2.Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)")
    req.add_header("accept", "*/*")
    req.add_header("connection", "Keep-Alive")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return res


def save_value(params):
    '''
    1:00000000001447171200:04611686018427387904:09223372036854775804:04611686018427387904
    time_line = 04611686018427387904
    minus4 = 9223372036854775804
    timestamp = 1447171200
    '''
    time_line = '04611686018427387904'
    minus8 = 9223372036854775800
    timestamp = start_timestamp
    count = 0

    likes, follwers = scrape_like_follow_of_url(params[0])
    params[2] = likes
    params[3] = follwers

    while count <= MAX_PAGE_COUNT and not stop:
        try:
            response, url = get_req(page_id, time_line, minus8, timestamp)
            response = response.replace("\n", "").replace("\r", "")
            photo_list, video_list, timestamp = get_first_four_column(response, url)
            if timestamp < stop_timestamp:
                break
            second_four_dict = get_second_four_without_video(response)
            print(len(photo_list), len(video_list), count)

            if video_list:
                view_count_dict = get_video_view_count(response)
            else:
                view_count_dict = {}

            for post in photo_list:
                if 'posts' in post[0]:
                    key = post[0].split('/')[-1]
                else:
                    key = post[0].split('/')[-2]
                details = second_four_dict.get(key)
                if details:
                    one_row = params + post[:3] + details + ['N/A']
                    print one_row
                    alldata.append(one_row)
            for post in video_list:
                if 'posts' in post[0]:
                    key = post[0].split('/')[-1]
                else:
                    key = post[0].split('/')[-2]
                details = second_four_dict.get(key, ['N/A', 'N/A', 'N/A'])
                if details:
                    one_row = params + post + details + [view_count_dict.get(key, 0)]
                    print one_row
                    alldata.append(one_row)
            minus8 -= 8
            count += len(photo_list) + len(video_list)
        except Exception as e:
            print(e)
            minus8 -= 8


def write_excel(filename, alldata, flag=None):
    filename = 'data/' + filename
    if flag:
        filename = filename.replace('.xls', '_' + str(flag) + '.xls')
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)
    w = xlwt.Workbook(encoding='utf-8')
    ws = w.add_sheet('old', cell_overwrite_ok=True)
    for row in range(0, len(alldata)):
        one_row = alldata[row]
        for col in range(0, len(one_row)):
            try:
                ws.write(row, col, one_row[col][:32766])
            except:
                try:
                    ws.write(row, col, one_row[col])
                except:
                    print '===Write excel ERROR===' + str(one_row[col])
    w.save(filename)
    print filename + "===========over============"


def set_page_id(url):
    global page_id
    reg = 'page_id=(\d*)'
    html = get_ori_html(url)
    page_id = str(re.compile(reg).findall(html)[0])


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    for i in range(len(urls)):
        url = urls[i]
        try:
            print '=======start '+url[0]+' ========='
            filename = "" + url[0].split("/")[3].split("?")[0] + ".xls"
            set_page_id(url[0])
            save_value(url)
            write_excel(filename, alldata)
            del alldata
            stop = False
            alldata = [['Page Url', 'Page Name', 'No. likes', 'No. follows', 'Post Url', 'Date', 'Main Text', 'No. reactions', 'No. Comment', 'No. Shares', 'No. Views']]
        except Exception as e:
            print('EXCEPT', url[0])
