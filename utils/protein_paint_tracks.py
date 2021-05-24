#!/hpcf/apps/python/install/2.7.13/bin/python
from utils import *
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
def run_upload_tracks(jid,bw_files,bw_types,dir,genome):
	"""copy files to ppr_dir and create a json file for visualization

	input
	-----

	the structure is /username/jid/*.bw + *types*.json



	"""


	#---------------- initialize parameters ---------------------------------
	file = open(p_dir+"../share/misc/AT847CE", 'rb')
	password = pickle.load(file)
	file.close()
	ppr_dir = "/research/rgs01/resgen/legacy/gb_customTracks/tp/HemPipelines/"
	hostname = "10.220.19.183"
	username = "yli11"
	user_dir = "%s"%(ppr_dir)+username+"/"+jid+"/"	
	#------------------ connection -------------------------------------------	
	paramiko.util.log_to_file("/tmp/"+jid)
	logging.info( "connecting to server")
	ssh_client =paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	ssh_client.connect(hostname=hostname,username=username,password=password)

	#------------------------ user's data dir ---------------------------------
	if dir:
		logging.info( "creating user's dir")
		stdin,stdout,stderr=ssh_client.exec_command("mkdir %s"%(ppr_dir)+username)
		time.sleep(5)
		stdin,stdout,stderr=ssh_client.exec_command("mkdir %s"%(ppr_dir)+username+"/"+jid)
		time.sleep(5)	
	
	#------------------------- json file ---------------------------------------
	logging.info( "generating json file")
	tracks_template = '{"type":"bigwig","scale":{"auto": 1},"file": "{{relative_path}}","stackheight":20,"stackspace":1,"onerow":1,"name":"{{track_name}}"}'
	tmp_file = "/tmp/"+str(uuid.uuid4()).split("-")[-1]
	tmp_file_handle = open(tmp_file,"wb")
	tracks_json_list=[]
	for b in bw_files:
		tmp = tracks_template.replace("{{relative_path}}","HemPipelines/"+username+"/"+jid+"/"+b)
		tmp = tmp.replace("{{track_name}}",b.replace("."+bw_types,""))
		tracks_json_list.append(tmp)
	if "20copy" in genome:
		lines = open(p_dir+"../share/NGS_pipeline/hg19_20copy_template.json").readlines()
	else:
		lines = open(p_dir+"../share/NGS_pipeline/template2_browser.json").readlines()
	lines = "".join(lines)
	lines = lines.replace("{{genome_version}}",genome)
	lines = lines.replace("{{tracks_json_list}}",",\n".join(tracks_json_list))	
	print >>tmp_file_handle,lines
	tmp_file_handle.close()

	#---------------------------- transfering file ----------------------------
	logging.info( "transfering file")
	ftp_client=ssh_client.open_sftp()
	for b in bw_files:
		if isfile(b):
			logging.info( "trasferring",b)
			ftp_client.put(b,user_dir+b)
			time.sleep(5)
		else:
			logging.error( b,"not exist")
	ftp_client.put(tmp_file,user_dir+bw_types+".json")
	ftp_client.close()
	ssh_client.close()

	#-------------------------- return URL ---------------------------------------
	myURL = "https://ppr.stjude.org/?study=HemPipelines/UserName/UserJobID/{{tracks}}.json"
	myURL = myURL.replace("UserName",username)
	myURL = myURL.replace("UserJobID",jid)
	myURL = myURL.replace("{{tracks}}",bw_types)
	return myURL	


def upload_bed_bw(jid,dir,genome):
	"""copy files to ppr_dir and create a json file for visualization

	input
	-----

	the structure is /username/jid/*.bw + *types*.json



	"""


	#---------------- initialize parameters ---------------------------------
	file = open(p_dir+"../share/misc/AT847CE", 'rb')
	password = pickle.load(file)
	file.close()
	ppr_dir = "/research/rgs01/resgen/legacy/gb_customTracks/tp/HemPipelines/"
	hostname = "10.220.19.183"
	username = "yli11"
	user_dir = "%s"%(ppr_dir)+username+"/"+jid+"/"	
	#------------------ connection -------------------------------------------	
	paramiko.util.log_to_file("/tmp/"+jid)
	logging.getLogger("paramiko").setLevel(logging.WARNING)
	logging.info( "connecting to server")
	ssh_client =paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=hostname,username=username,password=password)

	#------------------------ user's data dir ---------------------------------
	if dir:
		logging.info( "creating user's dir")
		stdin,stdout,stderr=ssh_client.exec_command("mkdir %s"%(ppr_dir)+username)
		time.sleep(5)
		stdin,stdout,stderr=ssh_client.exec_command("mkdir %s"%(ppr_dir)+username+"/"+jid)
		time.sleep(5)	
	
	#------------------------- json file ---------------------------------------
	logging.info( "generating json file")
	tracks_template = '{"type":"bigwig","scale":{"auto": 1},"file": "{{relative_path}}","stackheight":20,"stackspace":1,"onerow":1,"name":"{{track_name}}"}'
	bed_track_template = '{"type":"bedj","name":"{{track_name}}","file":"{{relative_path}}","stackheight":10,"stackspace":1}'
	bedpe_track_template = '{"type":"hicstraw","name":"{{track_name}}","mode_arc":true,"mode_hm":false,"bedfile":"{{relative_path}}","enzyme":"MboI"}'
	tmp_file = "/tmp/"+str(uuid.uuid4()).split("-")[-1]
	tmp_file_handle = open(tmp_file,"wb")
	tracks_json_list=[]
	bw_types = "tracks"
	bw_files = glob.glob("*.bw")
	

	
	# bed_process_command = """for i in *.bed;do awk 'BEGIN{FS=OFS="\\t"} {print $1,$2,$3,"{\\"strand\\":\\"+\\"}"}' $i > $i.bed3;sort -k1,1 -k2,2n $i.bed3 > $i.sorted;bgzip $i.sorted;tabix -p bed $i.sorted.gz;done"""
	bed_process_command = """for i in *.bed;do bed_to_bedjs_color_by_strand.py $i;done"""
	peak_process_command = """for i in *Peak;do awk 'BEGIN{FS=OFS="\\t"} {print $1,$2,$3,"{\\"strand\\":\\"+\\"}"}' $i > $i.bed3;sort -k1,1 -k2,2n $i.bed3 > $i.sorted;bgzip $i.sorted;tabix -p bed $i.sorted.gz;done"""
	bedpe_process_command = """for i in *bedpe;do awk 'BEGIN{FS=OFS="\\t"} {print $1,$2,$3,$4,$5,$6,$7}' $i > $i.bedpe3;sort -k1,1 -k2,2n $i.bedpe3 > $i.interaction;bgzip $i.interaction;tabix -p bed $i.interaction.gz;done"""
	mango_process_command = """for i in *mango;do awk 'BEGIN{FS=OFS="\\t"} {print $1,$2,$3,$4,$5,$6,$7}' $i > part1;awk 'BEGIN{FS=OFS="\\t"} {print $4,$5,$6,$1,$2,$3,$7}' $i > part2;cat part1 part2 > $i.bedpe3;rm part1;rm part2;sort -k1,1 -k2,2n $i.bedpe3 > $i.interaction;bgzip $i.interaction;tabix -p bed $i.interaction.gz;done"""
	# mango_process_command = """for i in *mango;do awk 'BEGIN{FS=OFS="\\t"} {print $1,$2,$3,$4,$5,$6,$7}' $i > $i.bedpe3;sort -k1,1 -k2,2n $i.bedpe3 > $i.interaction;bgzip $i.interaction;tabix -p bed $i.interaction.gz;done"""
	if len(glob.glob("*bed"))>0:
		os.system(bed_process_command)
	if len(glob.glob("*Peak"))>0:
		os.system(peak_process_command)
	if len(glob.glob("*bedpe"))>0:
		os.system(bedpe_process_command)
	if len(glob.glob("*mango"))>0:
		os.system(mango_process_command)
	
	
	
	
	bed_index_files = glob.glob("*.sorted.gz.tbi")
	bedpe_index_files = glob.glob("*.interaction.gz.tbi")
	bed_gz_files = [x.replace(".tbi","") for x in bed_index_files]
	bedpe_gz_files = [x.replace(".tbi","") for x in bedpe_index_files]
	bed_files = bed_gz_files+bed_index_files
	bedpe_files = bedpe_gz_files+bedpe_index_files
	# print (bed_files)
	for b in bw_files:
		tmp = tracks_template.replace("{{relative_path}}","HemPipelines/"+username+"/"+jid+"/"+b)
		tmp = tmp.replace("{{track_name}}",b.replace(".bw",""))
		tracks_json_list.append(tmp)
	for b in bed_gz_files:
		tmp = bed_track_template.replace("{{relative_path}}","HemPipelines/"+username+"/"+jid+"/"+b)
		tmp = tmp.replace("{{track_name}}",b.replace(".sorted.gz",""))
		tracks_json_list.append(tmp)
	for b in bedpe_gz_files:
		tmp = bedpe_track_template.replace("{{relative_path}}","HemPipelines/"+username+"/"+jid+"/"+b)
		tmp = tmp.replace("{{track_name}}",b.replace(".interaction.gz",""))
		tracks_json_list.append(tmp)
	if "20copy" in genome:
		lines = open(p_dir+"../share/NGS_pipeline/hg19_20copy_template.json").readlines()
	else:
		lines = open(p_dir+"../share/NGS_pipeline/template2_browser.json").readlines()
	lines = "".join(lines)
	lines = lines.replace("{{genome_version}}",genome)
	lines = lines.replace("{{tracks_json_list}}",",\n".join(tracks_json_list))	
	print >>tmp_file_handle,lines
	
	
	
	

	#---------------------------- transfering file ----------------------------
	logging.info( "transfering file")
	ftp_client=ssh_client.open_sftp()
	for b in bw_files+bed_files+bedpe_files:
		if isfile(b):
			logging.info( "trasferring: %s"%(b))
			ftp_client.put(b,user_dir+b)
			time.sleep(5)
		else:
			logging.error( b,"not exist")
	tmp_file_handle.close()
	ftp_client.put(tmp_file,user_dir+bw_types+".json")
	ftp_client.close()
	ssh_client.close()

	#-------------------------- return URL ---------------------------------------
	myURL = "https://ppr.stjude.org/?study=HemPipelines/UserName/UserJobID/{{tracks}}.json"
	myURL = myURL.replace("UserName",username)
	myURL = myURL.replace("UserJobID",jid)
	myURL = myURL.replace("{{tracks}}",bw_types)
	return myURL	
