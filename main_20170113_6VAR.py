#################
# Menghitung nilai Effort software dengan metode analogi dan pendekatan use case
# Mencari software yang mirip
#
# data training	: ucp.csv
# data uji 		: uji.csv
#
# kolom pada data terdiri dari
# ProjectNo 	= nomor proyek
# uaw			= unadjust actor weight
# uucw 			= unadjusted use case weight
# tcf 			= Technical complexity factor
# ef 			= environmental factor
# ActualEffort 	= actual effort
#
# Metode klasifikasi: K-Nearest Neighbours
# Perhitungan jarak	: Euclidean Distance
################

# Import Library
import math
import csv
import numpy

# Inisiasi variabel awal
fileDataTraining = "ucp.csv"			# File csv Data Training
fileDataTesting = "uji.csv"				# File csv Data Uji/Testing
fileDataOutput = 'output.csv'			# File csv Data Output

# Variabel List 'Data Training'
uaw = []		# List untuk menampung kolom UAW
uucw = []		# List untuk menampung kolom UUCW
tcf = []		# List untuk menampung kolom TCF
ef = []			# List untuk menampung kolom EF
effort = []		# List untuk menampung kolom EFFORT

dt = 0.00		# Jumlah Record Data Training

uaw_max = 0.00		# Variabel menampung nilai maximum dari List UAW 
uucw_max = 0.00		# Variabel menampung nilai maximum dari List UUCW
tcf_max = 0.00		# Variabel menampung nilai maximum dari List TCF
ef_max = 0.00		# Variabel menampung nilai maximum dari List EF

uaw_normal = []		# List menampung nilai normal dari List UAW 
uucw_normal = []	# List menampung nilai normal dari List UUCW
tcf_normal = []		# List menampung nilai normal dari List TCF
ef_normal = []		# List menampung nilai normal dari List EF

# Inisialisasi parameter untuk 'Data Testing'
uaw_uji = []		# List untuk menampung kolom UAW
uucw_uji = []		# List untuk menampung kolom UUCW
tcf_uji = []		# List untuk menampung kolom TCF
ef_uji = []			# List untuk menampung kolom EF
effort_uji = []		# List untuk menampung kolom EFFORT

du = 0.00			# Jumlah Record Data Uji/Testing

uaw_uji_normal = []		# List menampung nilai normal dari List UAW 
uucw_uji_normal = []	# List menampung nilai normal dari List UUCW
tcf_uji_normal = []		# List menampung nilai normal dari List TCF
ef_uji_normal = []		# List menampung nilai normal dari List EF 

print "\n"
print "====================================================="
print "###       Menghitung nilai Effort software        ###"
print "### dengan metode analogy dan pendekatan use case ###"
print "====================================================="
print "\n"

# 1. Read csv file
reader_datalatih=csv.reader(open(fileDataTraining,"rb"),delimiter=',')
x = list(reader_datalatih)
result = numpy.array(x).astype('float')

# 2. Create List/Array for Parameter Training Data
# 2.2 Fill Parameter with data from csv file
counter = 0
recordCount = len(x)	# number of rows in csv file (data latih)
while counter <= recordCount-1:	 
	uaw.append(result[counter,1])		# 1 is UAW column
	uucw.append(result[counter,2])		# 2 is UUCW column
	tcf.append(result[counter,3])		# 3 is TCF column
	ef.append(result[counter,4])		# 4 is EF column
	effort.append(result[counter,5])	# 5	is Actual Effort Column
	counter = counter+1

# 3. Tampung nilai maximum dari setiap parameter
uaw_max = max(uaw) 
uucw_max = max(uucw)
tcf_max = max(tcf)
ef_max = max(ef)

dt = recordCount

# 4. Buat bentuk normal dari data latih/Training
counter = 0
while counter <= recordCount-1:
	uaw_normal.append(uaw[counter]/uaw_max)
	uucw_normal.append(uucw[counter]/uucw_max)
	tcf_normal.append(tcf[counter]/tcf_max)
	ef_normal.append(ef[counter]/ef_max)
	counter = counter+1

# 5. Project Baru
reader_datauji=csv.reader(open(fileDataTesting,"rb"),delimiter=',')
y=list(reader_datauji)
data_uji=numpy.array(y).astype('float')

# 5.2 Tampung data uji
counter = 0
jumlah_data_uji = len(y)
while counter <= jumlah_data_uji-1:
	uaw_uji.append(data_uji[counter,1])
	uucw_uji.append(data_uji[counter,2])	
	tcf_uji.append(data_uji[counter,3])		
	ef_uji.append(data_uji[counter,4])
	effort_uji.append(data_uji[counter,5])
	counter = counter+1
du = jumlah_data_uji

# 6. Buat bentuk normal untuk data uji
counter = 0
while counter <= jumlah_data_uji-1:
	uaw_uji_normal.append(uaw_uji[counter]/uaw_max)
	uucw_uji_normal.append(uucw_uji[counter]/uucw_max)
	tcf_uji_normal.append(tcf_uji[counter]/tcf_max)
	ef_uji_normal.append(ef_uji[counter]/ef_max)
	counter = counter+ 1
#print(ef_uji_normal)

def hapusCsv(fileName):					# Reset file csv
	filecsv = open(fileName, 'w')
	filecsv.close()

def ujiData(x):
# 7. Hitung jarak Euclidean antara data uji dan data latih
# 	 dan menghitung bobot
	uaw_distance = []			# distance for uaw
	uucw_distance = []			# distance for uucw
	tcf_distance = []			# distance for tcf
	ef_distance = []			# distance for ef
	total_distance = []			# total nilai dari eucledian distance
	index_awal = []				# index awal list supaya tidak dipengaruhi sorting
	rows = len(uaw_normal)-1   	# rows = jml index data latih
	project_uji_ke = x			# Project uji ke
	counter = 0
	while counter <= rows:
		"""
		# Euclidean distance normal
		p1 = (uucp_uji_normal[project_uji_ke]-uucp_normal[counter])**2
		p2 = (tcf_uji_normal[project_uji_ke]-tcf_normal[counter])**2
		p3 = (ef_uji_normal[project_uji_ke]-ef_normal[counter])**2
		"""
		# Euclidean distance with weight
		p1 = ((uaw_uji_normal[project_uji_ke]-uaw_normal[counter])/1)**2
		p2 = ((uucw_uji_normal[project_uji_ke]-uucw_normal[counter])/1)**2
		p3 = ((tcf_uji_normal[project_uji_ke]-tcf_normal[counter])/1)**2
		p4 = ((ef_uji_normal[project_uji_ke]-ef_normal[counter])/1)**2
		uaw_distance.append(p1)		# distance for uaw
		uucw_distance.append(p2)	# distance for uucw
		tcf_distance.append(p3)		# distance for tcf
		ef_distance.append(p4)		# distance for ef
		p5 = math.sqrt(p1+p2+p3+p4)	# p5 is a total distance
		# p6 = 1/p5					# p6 merupakan rumus menghitung similarity (Aha,) // JELEK..
		total_distance.append(p5)	# variabel untuk disorting
		index_awal.append(p5)		# untuk mempertahankan index data awal
		#print p4
		counter = counter+1

	print(".. Proccess data %d .. "% x)

	# 8. Pengurutan babot dari bobot terkecil 
	sorter = total_distance		# variabel sorter mengambil nilai list total_distance
	sorter.sort()				# melakukan pengurutan data dar yang terkecil


	# 
	n1 = index_awal.index(sorter[0])	# mengambil index terkecil
	n2 = index_awal.index(sorter[1])	# mengambil index terkecil ke-2
	n3 = index_awal.index(sorter[2])	# mengambil index terkecil ke-3
	n4 = index_awal.index(sorter[3])	# mengambil index terkecil ke-4
	n5 = index_awal.index(sorter[4])	# mengambil index terkecil ke-5

	eff_1 = effort[n1]		# Mengambil nilai effort pada index n1
	eff_2 = effort[n2]		# Mengambil nilai effort pada index n2
	eff_3 = effort[n3]		# Mengambil nilai effort pada index n3
	eff_4 = effort[n4]		# Mengambil nilai effort pada index n4
	eff_5 = effort[n5]		# Mengambil nilai effort pada index n5

	eff_3nn = (eff_1+eff_2+eff_3)/3 			# 3nn with mean adaptation
	eff_5nn = (eff_1+eff_2+eff_3+eff_4+eff_5)/5 # 5nn with mean adaptation 


	# Perhitungan IDW Method
	w1 = 1/sorter[0]**2
	w2 = 1/sorter[1]**2
	w3 = 1/sorter[2]**2
	w4 = 1/sorter[3]**2
	w5 = 1/sorter[4]**2


	v1 = w1*eff_1
	v2 = w2*eff_2
	v3 = w3*eff_3
	v4 = w4*eff_4
	v5 = w5*eff_5

	tw3nn = w1+w2+w3
	tv3nn = v1+v2+v3
	idw3nn = tv3nn/tw3nn

	tw5nn = w1+w2+w3+w4+w5
	tv5nn = v1+v2+v3+v4+v5
	idw5nn = tv5nn/tw5nn

	print("1nn	: %.2f" %eff_1)
	print("3nn 	: %.2f" %eff_3nn)
	print("5nn 	: %.2f" %eff_5nn)
	print("idw3nn	: %.2f" %idw3nn)
	print("idw5nn	: %.2f" %idw5nn)
	
	"""
	print "Effort 1 = %.2f" % eff_1
	print "Effort 2 = %.2f" % eff_2
	print "Effort 3 = %.2f" % eff_3
	print "Effort 4 = %.2f" % eff_4
	print "Effort 5 = %.2f" % eff_5
	print "\n"
	print "Effort 3nn = %.2f" % eff_3nn
	print "Effort 5nn = %.2f" % eff_5nn
	"""

	databaru = []	# List untuk menampung hasil estimasi

	databaru.append(eff_1)
	databaru.append(eff_3nn)
	databaru.append(eff_5nn)
	databaru.append(idw3nn)
	databaru.append(idw5nn)

	# Kirim hasil ke file output
	filecsv = open(fileDataOutput, 'a')
	datafile = csv.writer(filecsv)
	datafile.writerow(databaru)
	filecsv.close()

#########################################################
# Eksekusi Program
#########################################################
print "# Jumlah data training	: %d" % dt
print "# Jumlah data Uji 	: %d" % du
print("Prepare ..\n")

# Reset output file / Hapus isinya jika ada
hapusCsv(fileDataOutput)

# Kalkulasi semua Data Uji/Testing
counter = 0							# Index untuk data uji
while counter < du:
	ujiData(counter)				# Eksekusi perhitungan 
	counter+=1
print("\nProccess Done..!")
print("Estimation created in \'output.csv\'' file ..")


##########################################################