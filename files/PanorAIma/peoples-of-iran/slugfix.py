# robust github-style slug with NO high-unicode literals in source
ASCII_PUNCT=set("\\'!\"#$%&()*+,./:;<=>?@[]^`{|}~")
def slug(v):
    out=[]
    for ch in v:
        if ch.isspace():
            out.append('-'); continue
        o=ord(ch)
        if 0x2000<=o<=0x206F or 0x2E00<=o<=0x2E7F or o==0x2019 or ch in ASCII_PUNCT:
            continue
        out.append(ch.lower())
    return ''.join(out)
if __name__=="__main__":
    assert slug("هرکس از مردم خودش حرف می‌زند")=="هرکس-از-مردم-خودش-حرف-میزند", slug("هرکس از مردم خودش حرف می‌زند")
    print("slug OK:", slug("قومیت؛ لایه حافظه، نه واحد اصلی تحلیل امروز"))
