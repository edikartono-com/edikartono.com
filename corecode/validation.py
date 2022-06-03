from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
only_latters = RegexValidator('[a-zA-Z,.\s]+$', 'Pastikan hanya huruf, spasi, titik, dan koma')
phone_number = RegexValidator(
    r'^(?:07|08|\+?628)\s?(?:\d\s?){6,12}',
    "Nomor HP diawali: 628 or 08 or 07. Minimal 8 digit"
)

def _sizeof_file(img_size):
    i = 0
    while img_size > 1024 and i < len(suffixes)-1:
        img_size /= 1024
        i += 1
    f = ('%.2f' % img_size).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

def image_validator(cleaned_data, img_field, img_size):
    """
    Validator image size.

    Args:
        cleaned_data: return dari input yang divalidasi dan dikembalikan sebagai object
        img_field: nama field gambar (ImageField)
        img_size: batas ukuran file (dalam byte) terbesar yang diijinkan untuk diupload.
    
    Returns:
        Apabila ukuran gambar lebih kecil atau sama dengan img_size, gambar akan disimpan.
        Jika gambar lebih besar dari img_size, menampilkan pesan error bahwa gambar ukurannya 
        terlalu besar.
    """
    img_get = cleaned_data.get(img_field, None)
    humanize = _sizeof_file(img_size)
    if img_get:
        imgsize = float(img_get.size / 1048576)
        if img_get.size > img_size:
            raise ValidationError(
                "Maks file berukuran "+ humanize +", file kamu %.2f MB" % imgsize
            )
        return img_get
    else:
        raise ValidationError("Silahkan pilih gambar terlebih dahulu")

def only_number(minnum, maxnum):
    regex = r'^[0-9]{' + str(minnum) + ',' + str(maxnum) + '}$'
    return RegexValidator(
        regex,
        'Pastikan hanya angka. {min} sampai {max} digit'.format(min=minnum, max=maxnum)
    )