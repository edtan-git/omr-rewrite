""" handle database query """
import mysql.connector

def insertToEkstraksi(database_conn):
    cursor = database_conn.cursor()

    cursor.execute("INSERT INTO ekstraksi (id_gambar, nama, nomor_siswa, tanggal_lahir, paket_soal, skor)")