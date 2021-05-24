import sys
import re
from collections import defaultdict
import re
import operator
import os
print (os.__file__)
import fire


class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class msa_ploter():
    def __init__(self, width=1000, height=1000, text_anchor="end"):
        self.width = width
        self.height = height
        self.svg = '''<svg xmlns='http://www.w3.org/2000/svg' version='1.1' width='%s' height='%s' > \
        <style>
        text {
                text-anchor: middle;
                font-size: 10px;
                font-weight: bold;
                font-family: 'Times New Roman';
        }
        .top { stroke-dasharray: 0,10,30 }
        .left { stroke-dasharray: 30,10 }
        .bottom { stroke-dasharray: 20,10 }
        .right { stroke-dasharray: 10,10,20 }
        .sample_name { text-anchor: %s }
        </style>\n''' % (width, height, text_anchor)
        print ("start msa_ploter")
    def plot(self, sort_by_file='', align='', formats='aln', types='nuc' , x_start_shift=200,
             y_start_shift=20,
             bp_numbers_in_one_line=100,
             sort_list='',
             prefix="out",
             output_svg_tag="yes",
             bg_color="grey",
             A_font_color="black",
             A_bg_color="green",
             T_font_color="black",
             T_bg_color="blue",
             C_font_color="black",
             C_bg_color="red",
             G_font_color="black",
             G_bg_color="yellow",
             N_font_color="black",
             N_bg_color="white",
             gaps_of_fragments=3): # gaps_of_fragments =0 mean somethings
        outname = prefix+".svg"
        formats = str(formats)
        types = str(types)
        sort = self.parse_sort_file(sort_by_file, sort_list)
        self.parse_align(align, formats, types)
        self.plot_align(x_start_shift=x_start_shift, y_start_shift=y_start_shift,
                        bp_numbers_in_one_line=bp_numbers_in_one_line, sort_sample_list=sort,
                        output_svg_tag=output_svg_tag, bg_color=bg_color, A_font_color=A_font_color,
                        A_bg_color=A_bg_color, T_font_color=T_font_color, T_bg_color=T_bg_color,
                        C_font_color=C_font_color, C_bg_color=C_bg_color, G_font_color=G_font_color,
                        G_bg_color=G_bg_color, N_font_color=N_font_color, N_bg_color=N_bg_color,
                        gaps_of_fragments=gaps_of_fragments
                        )
        self.write2svg(outname)



    def parse_align(self, malign, formats, types):
        if formats == "aln":
            print (f"start parse aln {types}")

            self.alns, self.seq_len = self.read_aln(malign, types)
            #print (f"alns is {self.alns}")
            #print ("seq lenis %s " % (self.seq_len))
        else:
            sys.exit(print (f"error:not support {formats} yet"))
    def read_aln(self, mlign, types):
        seq_len = 0
        alns = AutoVivification()
        if types == 'nuc':
            print ("start parse aln nuc")
            index = 0
            with open(mlign, 'r') as mf:
                for line in mf:
                    line = line.strip()
                    if line == '':
                        index = 0
                        continue
                    m = re.match(r"^(.*)\s+([ATCGatcg-]+)$", line)
                    if m:
                        #print ("line %s type:%s " % (line, type(line)))
                        sample_name, seq = m.group(1, 2)
                        sample_name = sample_name.strip()
                        if re.search('a', seq): seq = re.sub('a', 'A', seq)
                        if re.search('t', seq): seq = re.sub('t', 'T', seq)
                        if re.search('c', seq): seq = re.sub('c', 'C', seq)
                        if re.search('g', seq): seq = re.sub('g', 'G', seq)
                        if re.search('n', seq): seq = re.sub('g', 'N', seq)
                        alns[sample_name]['index'] = index
                        if not alns[sample_name]['seq']: alns[sample_name]['seq'] = ""
                        alns[sample_name]['seq'] += seq
                        if index == 0: seq_len += len(seq)
                        index += 1

            return alns, seq_len
        elif types == 'pep':
            sys.exit(print ("error:not support parse aln pep yet"))
        else:
            sys.exit(print ("error:not support parse aln {types} yet"))
    def plot_align(self, x_start_shift=0, y_start_shift=0, bp_numbers_in_one_line=1000,
                    output_svg_tag="yes", bg_color="grey",
                    A_font_color="black", A_bg_color="green", T_font_color="black", T_bg_color="blue",
                    C_font_color="black",C_bg_color="red",G_font_color="black",G_bg_color="yellow",
                    N_font_color="black",N_bg_color="white", sort_sample_list=None, gaps_of_fragments=3): # gaps_of_fragments =0 mean somethings
        x_start_shift = int(x_start_shift)
        y_start_shift = int(y_start_shift)
        bp_numbers_in_one_line = int(bp_numbers_in_one_line)
        gaps_of_fragments = int(gaps_of_fragments)
        if self.seq_len % bp_numbers_in_one_line:
            fragments = int(self.seq_len/bp_numbers_in_one_line+1)
        else:
            fragments = self.seq_len/bp_numbers_in_one_line

        #print ("height is %s,type is %s" % (self.height, type(self.height)))
        self.A_font_color = A_font_color
        self.A_bg_color = A_bg_color
        self.T_font_color = T_font_color
        self.T_bg_color = T_bg_color
        self.C_font_color = C_font_color
        self.C_bg_color = C_bg_color
        self.G_font_color = G_font_color
        self.G_bg_color = G_bg_color
        self.N_font_color = N_font_color
        self.N_bg_color = N_bg_color

        line_height = self.height/(fragments*(len(self.alns.keys())+ gaps_of_fragments))
        #print (f"height:{self.height};line_height:{line_height};")
        ss = []
        if sort_sample_list:
            ss = sort_sample_list
        else:
            ss = [ k for k,w in sorted(self.alns.items(), key=lambda kv: kv[1]['index'])] #sort dict by value
        for i in range(fragments):
            j=0
            lens = [len(x) for x in ss]
            max_len = max(lens)*1.1 ## sample name left margin = 1.1 - 1 = 0.1
            for sample in ss:
                self.svg += self.plot_one_line(sample_name_x_start=max_len, sample=sample, x_start=x_start_shift,
                                            #y_start=y_start_shift+(i*len(ss)+1+j)*line_height,
                                            y_start=y_start_shift + (i*(len(ss)+gaps_of_fragments)+j)*10,
                                            seq=self.alns[sample]['seq'],
                                            start=bp_numbers_in_one_line*i,
                                            end=bp_numbers_in_one_line*(i+1)-1)
                j +=1
        self.svg +="</svg>\n"

    def plot_one_line(self, seq=None, start=None, end=None, **kwargs):
        x_start = kwargs['x_start']
        y_start = kwargs['y_start']
        sample_name_x_start = kwargs['sample_name_x_start']
        padding_sample_name = 15
        sample = kwargs['sample']
        fragment = self.alns[sample]['seq'][start:end+1]
        font_color = bg_color = line = ''
        max_len = 1
        line += f"<text x='{x_start-padding_sample_name}' y='{y_start+9}' class ='sample_name'>{sample}</text>"
        for base in fragment:
            if base == "A": font_color, bg_color = self.A_font_color, self.A_bg_color
            if base == "T": font_color, bg_color = self.T_font_color, self.T_bg_color
            if base == "C": font_color, bg_color = self.C_font_color, self.C_bg_color
            if base == "G": font_color, bg_color = self.G_font_color, self.G_bg_color
            if base == "-": font_color, bg_color = self.N_font_color, self.N_bg_color

            line += f"<rect  x='{x_start}' y='{y_start}' width='10'  height='10' style='fill:{bg_color};stroke:black;stroke-width:0.1;fill-opacity:0.3;stroke-opacity:0.9' /> \
            <text x='{x_start+5}' y='{y_start}' dy='9' fill='{font_color}' textLength='10'>{base}</text>\n"
            x_start +=10

        #line = f"<text x='{x_start}' y='{y_start}' font-size='10px'>    \
        #<tspan font-style='normal' fill='red'>{sample}</tspan> \
        #<tspan fill='green'>{fragment}</tspan></text>\n"
        return line
    def write2svg(self,outfile):
        with open(outfile, 'w') as f:
            f.write(self.svg)
        print (f"write to file: {outfile}\n")



    def parse_sort_file(self, sort_file, sort_list):
        sort = []
        sort_list = str(sort_list)
        if sort_file:
            with open(sort_file) as f:
                for line in f:
                    f = f.strip()
                    if f == "": continue
                    sort.append(f)
        if sort == [] and sort_list:
            if re.search(",", sort_list):
                sort = sort_list.split(",")
            else:
                sys.exit(print (f"error: sort_list {sort_list}"))
        return sort


if __name__ == "__main__":
    fire.Fire(msa_ploter)

