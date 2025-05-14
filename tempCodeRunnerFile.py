from flask import Flask, render_template, request
from dataset import makanan_dataset 

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rekomendasi', methods=['POST'])
def rekomendasi():
    diet = request.form.get('diet')
    tujuan = request.form.get('tujuan')
    waktu = request.form.get('waktu')
    alergi_input = request.form.get('alergi', '')
    kalori_maks = request.form.get('kalori')

    alergi = [a.strip().lower() for a in alergi_input.split(',') if a.strip()]
    kalori_maks = int(kalori_maks) if kalori_maks else None

    rekomendasi = []

    for makanan in makanan_dataset:
        if makanan['diet'] != diet:
            continue
        if tujuan.lower() not in [tuju.lower() for tuju in makanan['cocok_untuk']]:
            continue
        if waktu and waktu.lower() not in [w.lower() for w in makanan.get('waktu', [])]:
            continue
        if any(a in [al.lower() for al in makanan['alergi']] for a in alergi):
            continue
        if kalori_maks is not None and makanan['kalori'] > kalori_maks:
            continue
        rekomendasi.append(makanan)

    # Urutkan berdasarkan kalori terendah
    rekomendasi.sort(key=lambda x: x['kalori'])

    return render_template('result.html', hasil=rekomendasi)

if __name__ == '__main__':
    app.run(debug=True)
