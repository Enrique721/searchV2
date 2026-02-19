import re

pattern = re.compile(
    r'^(?:([a-zA-Z][a-zA-Z0-9+.-]*:\/\/[^\s]+)\s*[:\s]+)?'
    r'((?:\+?\d{1,3})?\d{8,15}|[a-zA-Z0-9._-]+(?:@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})?)'
    r'\s*[:\s]+\s*'
    r'([^\s\x00-\x1F\x7F█╔╗╝╚═]+)$'
)



samples = [
    "https://site.com admin:123456",
    "https://site.com sadkff@asdal.aaa Pyjr4xLZN",
    "root toor",
    "+5511987654321:senha123",
    "https://corp.com +15551234567 P@ssw0rd!",
    "██╔══██╗██╔══██╗██║████╗ ██║╚══███╔╝██╔═══██╗╚════██║",  # lixo
    "https://accounts.google.com/:yaaskie:28102004Alya",
    "android://RGlUtI9NY0ps7eW1mdYoROkaZ3iIqThRr1OIJOwe5lqdRX93aUt2TxUUz13PLlTFN5B1C0mMDPyM4BsBic8Fmg==@com.roblox.client:phatdoge:pass",
    "https://thanhtoanhocphi.epu.edu.vn/something/Login:19810710036:pass"
]

for line in samples:
    m = pattern.match(line)
    if not m:
        print("❌ NO MATCH:", line)
        continue

    url, user, password = m.groups()
    print("✅ MATCH")
    print("   url     :", url)
    print("   user    :", user)
    print("   password:", password)


# with open("telegram/consumeDir/leaked.txt", "r") as f:
#     for line in f:
#         m = pattern.search(line)
#         if m:
#             url, user, pwd = m.groups()
#             print(f"url={url}, user={user}, pwd={pwd}")


