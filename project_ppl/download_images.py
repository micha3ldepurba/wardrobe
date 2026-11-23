import os
import urllib.request

images_dir = "images"
os.makedirs(images_dir, exist_ok=True)

items = [
    # 10 Atasan Wanita (Warna & Model Berbeda)
    ("atasan_1_blouse_beige.jpg", "https://image.hm.com/assets/hm/e4/0e/e40e13266955c95592ab7f50d83f4dc35a099c01.jpg?imwidth=2160"),
    ("atasan_2_crop_top_cokelat.jpg", "https://livesozy.com/cdn/shop/files/lea-crop-top-top-1246217529.jpg?v=1782527887&width=960"),
    ("atasan_3_kaos_hitam.jpg", "https://createfashionbrand.com/wp-content/uploads/2024/07/Szm7L3jDCrApo0waurl6ib_5YoKHQvcIVGy7kLieUzQ-copia-3-1.webp"),
    ("atasan_4_kemeja_putih.jpg", "https://a.storyblok.com/f/110856/3500x4666/1bf386ad12/white-linen-shirt-5.jpg"),
    ("atasan_5_kaos_pink.jpg", "https://xcdn.next.co.uk/common/items/default/default/itemimages/3_4Ratio/product/lge/B77902s4.jpg?im=Resize,width=750"),
    ("atasan_6_sweater_navy.jpg", "https://imgproxy.johnhenric.com/preset:sharp/resize:fit:1250/gravity:nowe/quality:80/aHR0cHM6Ly9qb2huaGVucmljLmNlbnRyYWNkbi5uZXQvY2xpZW50L2R5bmFtaWMvaW1hZ2VzLzM1MDhfOWEzMDMzZTRmOS1hMDMxNDgtMDYtMDEtb3JpZ2luYWwuanBn"),
    ("atasan_7_overshirt_olive.jpg", "https://www.permanentstyle.com/wp-content/uploads/2022/05/valerio-linen-overshirt.jpg"),
    ("atasan_8_hoodie_abu.jpg", "https://scdn.speedsize.com/d31641c5-60cb-4a0b-8662-59094f81bb6e/https://au.representclo.com/cdn/shop/articles/Screenshot_2023-08-18_at_10.54.23.png?v=1705311710&width=1346"),
    ("atasan_9_denim_shirt_biru.jpg", "http://www.urbanofashion.com/cdn/shop/files/shirtdenovhfbowl-03-dblue-1_bc616b8a-091d-4824-ba36-df4bbec9efb2.jpg?v=1779089729"),
    ("atasan_10_kemeja_garis.jpg", "https://i0.wp.com/thefashionhousemom.com/wp-content/uploads/2025/08/Wide-leg-jeans-and-button-up-shirt-outfit.jpg?resize=600%2C900&ssl=1"),

    # 10 Bawahan Wanita (Model & Jenis Berbeda)
    ("bawahan_1_wide_leg_putih.jpg", "https://littleboxindia.com/cdn/shop/files/Pleated_High_Waisted_Wide_Leg_Trousers_in_Off-White_2048x.jpg?v=1769664650"),
    ("bawahan_2_rok_plisket_hitam.jpg", "https://www.jennikayne.com/cdn/shop/files/pleated-skirt-black_2cedf5d7-3aa9-4c8e-a27d-996df5f1467d.jpg?v=1786396642"),
    ("bawahan_3_rok_midi_denim.jpg", "https://static.e-stradivarius.net/assets/public/2b39/18e9/9c9b4eec810e/cbe33d3ca43c/04654217715-a15/04654217715-a15.jpg?ts=1786548092734&w=1082&f=auto"),
    ("bawahan_4_formal_navy.jpg", "https://i.etsystatic.com/64685441/r/il/36afea/8026876421/il_570xN.8026876421_9g7h.jpg"),
    ("bawahan_5_cargo_cokelat.jpg", "https://hourscollection.com/cdn/shop/files/BLUFFS_34.jpg?v=1728837712&width=2540"),
    ("bawahan_6_sweatpants_abu.jpg", "http://hillswear.com/cdn/shop/files/basic_sweatpants_grey_melange.jpg?v=1770549032"),
    ("bawahan_7_corduroy_merah_bata.jpg", "https://pumpsandpushups.com/wp-content/uploads/2025/09/7D6A9588.jpg"),
    ("bawahan_8_linen_shorts_putih.jpg", "https://www.legendlondon.co/cdn/shop/files/legend-london-short-summer-linen-short-white-1232546108.jpg?v=1776750643&width=3840"),
    ("bawahan_9_jeans_biru.jpg", "https://media.istockphoto.com/id/2143789264/photo/a-pile-of-blue-denim-jeans.jpg?s=612x612&w=0&k=20&c=qe6rnG5AYGEtRG0WSaCMSfpVJRfx0E_eQnpVHfgIikc="),
    ("bawahan_10_chinos_khaki.jpg", "https://executive.co.id/cdn/shop/files/1-LPRCRT126B274_KHAKI_2_800x800_a542b5b2-f3dd-4d5f-81c3-86e77617851e.jpg?v=1770109759")
]

req_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for fname, url in items:
    path = os.path.join(images_dir, fname)
    print(f"Downloading {fname}...")
    try:
        req = urllib.request.Request(url, headers=req_headers)
        with urllib.request.urlopen(req) as resp, open(path, 'wb') as f:
            f.write(resp.read())
        print(f"Successfully saved {fname}")
    except Exception as e:
        print(f"Failed {fname}: {e}")
