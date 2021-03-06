#!/hpcf/apps/python/install/2.7.13/bin/python
from utils import *
import os
import argparse
p_dir = os.path.dirname(os.path.realpath(__file__)) + "/"

def arg_volcano_plot(parser):
	cmd=parser.add_parser('volcano_plot',help='Data visualization: Volcano plot',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	cmd.add_argument('--short',  help="Force to use the short queue, don't use it for volcano_plot", action='store_true')	
	cmd.add_argument('--no_email',  help="Not for end-user", action='store_true')	

	cmd.add_argument('-f','--input',  help="data table to be plot", required=True)
	cmd.add_argument('-j',"--jid",  help="enter a job ID, which is used to make a new directory. Every output will be moved into this folder.", default='{{subcmd}}_'+username+"_"+str(datetime.date.today()))	

	options=cmd.add_argument_group(title='options')
	options.add_argument('-s','--seperator',  help='column seperator, comma(,), space(" "), or tab(\t)', default=',',type=str)
	options.add_argument('--LFC_column',  help="column name for log fold change", default='LFC',type=str)
	options.add_argument('--LFC_cutoff',  help="log fold change cutoff", default="2",type=str)
	options.add_argument('--LFC_axis_name',  help="The axis name for log fold change", default='LFC',type=str)
	options.add_argument('--FDR_column',  help="column name for p-value or FDR", default='FDR',type=str)
	options.add_argument('--FDR_cutoff',  help="p-value or FDR cutoff", default="0.01",type=str)
	options.add_argument('--FDR_axis_name',  help="The axis name for p-value or FDR", default='FDR',type=str)	
	options.add_argument('--title',  help="Figure title", default='Volcano plot',type=str)
	options.add_argument('--do_not_submit',  help="EnhancedVolcano is installed on rhel7 nodes, by default you are on rhel6 nodes, unless you did ``hpcf_interactive -q standard``, please don't use this option.", action='store_true')
	options.add_argument('--output_figure',  help="output file name", default='Volcano_plot_'+username+"_"+str(datetime.date.today())+".png",type=str)


def run_volcano_plot(args,rootLogger):
	# rootLogger.info("this is volcano_plot")
	# rootLogger.info(str(args.subcmd).lower())
	if str(args.subcmd).lower() != "volcano_plot":
		return 0		
	if not os.path.isfile(args.input):
		rootLogger.error("Input files do not exist!")
		os.system("HemTools volcano_plot -h")
		# rootLogger.close()
		os.system("rm "+args.jid+".log")
		sys.exit(1)
	if os.path.isdir(args.jid):
		addon_string = str(uuid.uuid4()).split("-")[-1]
		rootLogger.info ("The input job id is not available!")
		args.jid = args.jid+"_"+addon_string
		rootLogger.info ("The new job id is: "+args.jid)
	else:
		rootLogger.info ("The job id is: "+args.jid)			
		
	volcano_plot_command = "Rscript "+p_dir+"volcano_plot.R " + args.input\
							+' "'+args.seperator+'"'\
							+' "'+args.LFC_column+'"'\
							+' "'+args.LFC_cutoff+'"'\
							+' "'+args.LFC_axis_name+'"'\
							+' "'+args.FDR_column+'"'\
							+' "'+args.FDR_cutoff+'"'\
							+' "'+args.FDR_axis_name+'"'\
							+' "'+args.title+'"'\
							+' "'+args.output_figure+'"'
	command = "\n".join(['module load R/3.5.1',volcano_plot_command])

	# NGS_pipeline is a general class for submiting single command jobs
	volcano_plot = NGS_pipeline(args,rootLogger)

	outputDict = {}
	outputDict['figure'] = [args.output_figure,'Rplots.pdf']

	attachments = outputDict['figure']

	volcano_plot.submit_single_command(command,output_dict=outputDict,attachments=attachments)
	if args.no_email:
		volcano_plot.run_output_organization(report_flag=False,email_flag = False)
	else:
		volcano_plot.run_output_organization(report_flag=False)












