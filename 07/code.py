import argparse
from time import time

DAY = 7

PUZZLE_TEXT = '''
--- Day 7: No Space Left On Device ---

You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device
Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
cd / switches the current directory to the outermost directory, /.
ls means list. It prints out all of the files and directories immediately contained by the current directory:
123 abc means that the current directory contains a file named abc with size 123.
dir xyz means that the current directory contains a directory named xyz.
Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e which contains i).
Directory d has total size 24933642.
As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.
To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes. In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?

Your puzzle answer was 1454188.

--- Part Two ---

Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least 30000000. You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165; this means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required by the update. Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

Delete directory e, which would increase unused space by 584.
Delete directory a, which would increase unused space by 94853.
Delete directory d, which would increase unused space by 24933642.
Delete directory /, which would increase unused space by 48381165.
Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?

Your puzzle answer was 4183246.
'''

SAMPLE_INPUT = '''
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''

PUZZLE_INPUT = '''
$ cd /
$ ls
dir cmvqf
dir dcgbjvj
57426 gszshjwr.lrs
dir nsgms
124423 rjqns.prb
dir wqvv
$ cd cmvqf
$ ls
6852 cnsb.cmm
319810 cwqbmjb.vpl
dir dcgbjvj
dir ddnclwtd
dir gccnrw
dir qwzphd
dir rvqwnjv
dir ssmf
107040 trttdw.jsn
dir wcn
296426 wqvv
$ cd dcgbjvj
$ ls
dir dcgbjvj
dir rlvcvj
$ cd dcgbjvj
$ ls
214674 gsqcwfmz.hlm
$ cd ..
$ cd rlvcvj
$ ls
151752 cnsb.cmm
256829 sjlwgf.mqn
$ cd ..
$ cd ..
$ cd ddnclwtd
$ ls
177893 fpwznlp.zsf
$ cd ..
$ cd gccnrw
$ ls
dir mbfw
dir rlvcvj
dir wsrdh
dir wvq
dir zgpdl
$ cd mbfw
$ ls
dir dcgbjvj
dir mhnjvrl
271166 ptrv
$ cd dcgbjvj
$ ls
dir npjmq
$ cd npjmq
$ ls
26712 fpwznlp.zsf
$ cd ..
$ cd ..
$ cd mhnjvrl
$ ls
190094 mgrdrbl.lqg
199191 zgczmvng
22082 zgczmvng.rld
$ cd ..
$ cd ..
$ cd rlvcvj
$ ls
244617 mbjprm
264738 wpgglg
$ cd ..
$ cd wsrdh
$ ls
dir mgmp
111558 vnqmnjpb.bnc
$ cd mgmp
$ ls
dir whzjb
$ cd whzjb
$ ls
235442 mgrdrbl.lqg
63642 sphms.tzw
$ cd ..
$ cd ..
$ cd ..
$ cd wvq
$ ls
23240 dcgbjvj.rwc
79015 hcb
155120 jjc
dir wqvv
207559 wqvv.cwp
$ cd wqvv
$ ls
130961 cnsb.cmm
dir fcl
208524 hgbr.snf
dir lzs
14868 mgrdrbl.lqg
dir sqpgtrn
143653 zgczmvng
$ cd fcl
$ ls
dir jfjgnz
$ cd jfjgnz
$ ls
225416 trttdw.jsn
$ cd ..
$ cd ..
$ cd lzs
$ ls
111949 vtcmf
$ cd ..
$ cd sqpgtrn
$ ls
289955 cnsb.cmm
dir crstpjjv
dir dcgbjvj
6334 nwv.blw
dir vpnhcsfr
$ cd crstpjjv
$ ls
144739 jtcndb.wht
16215 qdccst.dsg
$ cd ..
$ cd dcgbjvj
$ ls
dir bnzmws
dir crstpjjv
82495 fjmbgql
248051 hlcwhnf
145452 qwzjc.sth
dir spmr
268967 wqvv
23371 wqvv.vdm
dir zgczmvng
$ cd bnzmws
$ ls
dir dcgbjvj
dir dgbtqdn
119626 pvgrqjf.ftq
204879 tscrpt.szt
$ cd dcgbjvj
$ ls
152171 msf.qhf
$ cd ..
$ cd dgbtqdn
$ ls
64965 fpwznlp.zsf
$ cd ..
$ cd ..
$ cd crstpjjv
$ ls
97804 mgrdrbl.lqg
88837 trttdw.jsn
$ cd ..
$ cd spmr
$ ls
302501 dcgbjvj
$ cd ..
$ cd zgczmvng
$ ls
dir crstpjjv
187957 prznqbn
$ cd crstpjjv
$ ls
218211 jlb.nvs
$ cd ..
$ cd ..
$ cd ..
$ cd vpnhcsfr
$ ls
220411 qtcdjgz
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd zgpdl
$ ls
dir llstdpv
dir rtftjm
$ cd llstdpv
$ ls
318556 qqccwwjf.mbw
$ cd ..
$ cd rtftjm
$ ls
117705 fwphh.zrz
$ cd ..
$ cd ..
$ cd ..
$ cd qwzphd
$ ls
dir crstpjjv
dir fvfmlgql
dir ldbts
dir ljtcgz
dir llvhbzpz
dir plcbgmwc
dir pwp
dir qjstb
58078 wmc
$ cd crstpjjv
$ ls
171196 sbf.vcc
320608 trttdw.jsn
$ cd ..
$ cd fvfmlgql
$ ls
dir hfdnml
298497 trttdw.jsn
$ cd hfdnml
$ ls
43441 crstpjjv.vrr
$ cd ..
$ cd ..
$ cd ldbts
$ ls
211746 crstpjjv
224627 rcw.rcl
$ cd ..
$ cd ljtcgz
$ ls
dir dfrnh
179456 fmbpcdbd.vrl
141254 fpwznlp.zsf
86291 pcmqcl.jmz
266763 pzvg.qcg
dir zjjbjn
$ cd dfrnh
$ ls
dir crstpjjv
$ cd crstpjjv
$ ls
220983 wqvv.hhn
$ cd ..
$ cd ..
$ cd zjjbjn
$ ls
215454 nwcbbv.mbb
$ cd ..
$ cd ..
$ cd llvhbzpz
$ ls
206731 cnsb.cmm
$ cd ..
$ cd plcbgmwc
$ ls
223141 fpwznlp.zsf
dir hplrsb
309856 jhdwr.jfc
dir mhmnmd
218364 mmfzhj.zvg
dir nwnj
316432 trttdw.jsn
dir vrgj
$ cd hplrsb
$ ls
dir lbscwd
dir lsffhj
dir mlfp
dir pqfbf
dir tcvjzzhj
dir wqvv
$ cd lbscwd
$ ls
157261 wvblz.hmp
$ cd ..
$ cd lsffhj
$ ls
171621 crstpjjv
$ cd ..
$ cd mlfp
$ ls
80994 vvjzm.pzt
$ cd ..
$ cd pqfbf
$ ls
67861 ltd.zbw
dir nnsg
dir nwcl
107828 rlvcvj
160956 trttdw.jsn
$ cd nnsg
$ ls
18252 tzcrqv.rsr
$ cd ..
$ cd nwcl
$ ls
38378 cnsb.cmm
217283 dqwpwzz
220081 mgrdrbl.lqg
28106 sbf.vcc
$ cd ..
$ cd ..
$ cd tcvjzzhj
$ ls
152965 dhv
316034 gvtdrj.rft
$ cd ..
$ cd wqvv
$ ls
281962 mfzf.nfn
95321 rlvcvj.zwf
$ cd ..
$ cd ..
$ cd mhmnmd
$ ls
213145 cnsb.cmm
dir hnzcz
273060 mnwhg
dir qcwdvq
318596 trttdw.jsn
$ cd hnzcz
$ ls
177795 fpwznlp.zsf
188898 rlvcvj
317234 wqvv.jsv
dir zgczmvng
$ cd zgczmvng
$ ls
dir qzfw
$ cd qzfw
$ ls
134097 rlvcvj
73145 sbf.vcc
$ cd ..
$ cd ..
$ cd ..
$ cd qcwdvq
$ ls
83084 wqvv
$ cd ..
$ cd ..
$ cd nwnj
$ ls
84366 hgpmqh
317603 mgrdrbl.lqg
$ cd ..
$ cd vrgj
$ ls
136595 fpwznlp.zsf
78517 sbf.vcc
dir wqvv
242465 wqvv.cpl
dir zln
$ cd wqvv
$ ls
3191 sbf.vcc
$ cd ..
$ cd zln
$ ls
dir crstpjjv
$ cd crstpjjv
$ ls
86511 btqgw
17597 rcstn.jpj
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd pwp
$ ls
dir crstpjjv
dir jlqdbv
290915 mgrdrbl.lqg
219909 nfgj
207313 sbf.vcc
dir zpjf
$ cd crstpjjv
$ ls
298992 crnfs.fgn
172934 jqh
$ cd ..
$ cd jlqdbv
$ ls
300436 zgczmvng
$ cd ..
$ cd zpjf
$ ls
78904 sbf.vcc
$ cd ..
$ cd ..
$ cd qjstb
$ ls
dir dtb
dir gcd
dir gmcnhh
85552 htm.lzc
219773 mzb.fvt
208419 schz
$ cd dtb
$ ls
167147 crstpjjv.zlb
$ cd ..
$ cd gcd
$ ls
239595 rlvcvj
$ cd ..
$ cd gmcnhh
$ ls
111653 fpwznlp.zsf
$ cd ..
$ cd ..
$ cd ..
$ cd rvqwnjv
$ ls
59215 cnsb.cmm
37164 jtlcr.rlm
dir mnc
$ cd mnc
$ ls
32159 cnsb.cmm
76204 trttdw.jsn
$ cd ..
$ cd ..
$ cd ssmf
$ ls
dir fvcd
127458 hpdzv
dir jcg
288242 jtjp.mjj
dir jzp
268857 mgrdrbl.lqg
223968 nhfmbvc
dir wqvv
235806 wqvv.fnl
$ cd fvcd
$ ls
26479 wcs.bdp
$ cd ..
$ cd jcg
$ ls
dir nsvtrs
dir zgczmvng
$ cd nsvtrs
$ ls
dir dcgbjvj
$ cd dcgbjvj
$ ls
36633 trttdw.jsn
$ cd ..
$ cd ..
$ cd zgczmvng
$ ls
221381 vszcg.jdb
$ cd ..
$ cd ..
$ cd jzp
$ ls
1957 dcgbjvj
$ cd ..
$ cd wqvv
$ ls
9330 wqvv.pvs
46963 ztlh
$ cd ..
$ cd ..
$ cd wcn
$ ls
dir cqdzdnq
dir cszzg
dir fqmcr
123361 pjfdtvzf.rdf
dir rmrg
dir rsfddzs
dir vqrpdwv
dir wpgddhdq
dir wpgv
$ cd cqdzdnq
$ ls
dir dqhpbsg
dir qlq
dir vfwhcpwl
dir wqvv
dir zpbbspcv
$ cd dqhpbsg
$ ls
245289 glbfq.vpw
51357 vsvvzbns.ftf
$ cd ..
$ cd qlq
$ ls
210318 mqgnjht.vqq
$ cd ..
$ cd vfwhcpwl
$ ls
109892 mmpzcjmp.znn
$ cd ..
$ cd wqvv
$ ls
dir chwdzfsg
dir crstpjjv
dir dcgbjvj
dir rllbccjt
dir rlvcvj
$ cd chwdzfsg
$ ls
108951 fpwznlp.zsf
dir vgc
$ cd vgc
$ ls
273011 fpwznlp.zsf
248078 ntc.ghp
77305 thgbb.mfn
73383 trttdw.jsn
$ cd ..
$ cd ..
$ cd crstpjjv
$ ls
dir qmswb
$ cd qmswb
$ ls
68252 trttdw.jsn
$ cd ..
$ cd ..
$ cd dcgbjvj
$ ls
111 qtcs.llc
dir szzthsmj
$ cd szzthsmj
$ ls
dir qhztdv
dir wqvv
dir zmqrftlm
$ cd qhztdv
$ ls
138433 qrdsrrb.chw
dir rlvcvj
$ cd rlvcvj
$ ls
dir jfcm
dir lzf
249984 rlvcvj.nmb
dir twrs
$ cd jfcm
$ ls
117884 dtrc.wsm
237577 rlvcvj.mhd
$ cd ..
$ cd lzf
$ ls
60342 nrc.clh
$ cd ..
$ cd twrs
$ ls
97201 cnsb.cmm
$ cd ..
$ cd ..
$ cd ..
$ cd wqvv
$ ls
73047 gcqzjf.gcb
$ cd ..
$ cd zmqrftlm
$ ls
dir ltd
$ cd ltd
$ ls
120673 fpwznlp.zsf
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd rllbccjt
$ ls
299611 cnsb.cmm
dir lnfvlqh
36418 qwh
dir rlvcvj
255907 trttdw.jsn
dir zqvzpv
$ cd lnfvlqh
$ ls
195010 fpwznlp.zsf
72496 llrznf.rwc
dir lvgzb
53126 mgrdrbl.lqg
90191 mnrqtn
310156 nthdm.crh
$ cd lvgzb
$ ls
209837 mgrdrbl.lqg
210074 rwhgmd
70338 sbf.vcc
$ cd ..
$ cd ..
$ cd rlvcvj
$ ls
252080 dcgbjvj
$ cd ..
$ cd zqvzpv
$ ls
249229 zpt.lbc
$ cd ..
$ cd ..
$ cd rlvcvj
$ ls
dir dcgbjvj
dir fdz
$ cd dcgbjvj
$ ls
191363 trttdw.jsn
$ cd ..
$ cd fdz
$ ls
291107 bqsdfc.rcn
dir dcgbjvj
64333 fpwznlp.zsf
dir lfb
280608 mgrdrbl.lqg
125554 trttdw.jsn
$ cd dcgbjvj
$ ls
169326 qwjhpdh
$ cd ..
$ cd lfb
$ ls
35299 zqfnjtr.clt
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd zpbbspcv
$ ls
54549 mgrdrbl.lqg
$ cd ..
$ cd ..
$ cd cszzg
$ ls
dir wqvv
$ cd wqvv
$ ls
136042 crstpjjv.jtq
10879 trttdw.jsn
$ cd ..
$ cd ..
$ cd fqmcr
$ ls
188798 bchvt.dvw
276819 fpwznlp.zsf
dir gdr
dir rlvcvj
5623 zgczmvng.fqs
158621 znddbv
$ cd gdr
$ ls
dir btg
213096 cnsb.cmm
dir dhbcmzbz
$ cd btg
$ ls
dir hjm
$ cd hjm
$ ls
144774 zgczmvng.llz
$ cd ..
$ cd ..
$ cd dhbcmzbz
$ ls
148108 rlvcvj
$ cd ..
$ cd ..
$ cd rlvcvj
$ ls
201103 qrdlf.pvg
272776 vnpgw.wts
153826 zgczmvng
290248 zgczmvng.gsv
$ cd ..
$ cd ..
$ cd rmrg
$ ls
dir jzb
dir nsslsw
dir rlvcvj
$ cd jzb
$ ls
273968 trttdw.jsn
$ cd ..
$ cd nsslsw
$ ls
226370 sbf.vcc
$ cd ..
$ cd rlvcvj
$ ls
294706 gsbqswjj
$ cd ..
$ cd ..
$ cd rsfddzs
$ ls
dir cphvtp
205384 crstpjjv
82103 dfrjwrnz.bfl
dir fntvngpm
297145 pqtrvd
237572 sbf.vcc
dir zgczmvng
$ cd cphvtp
$ ls
dir phvc
$ cd phvc
$ ls
52239 dcgbjvj.lbj
$ cd ..
$ cd ..
$ cd fntvngpm
$ ls
18297 mgrdrbl.lqg
$ cd ..
$ cd zgczmvng
$ ls
dir lzcwf
dir pqmc
179956 tzqjcn
dir zgczmvng
$ cd lzcwf
$ ls
284166 cnsb.cmm
157214 jhmmn.qwn
$ cd ..
$ cd pqmc
$ ls
215883 nlvdqw.jmt
dir qjfr
209722 wqvv.fgg
$ cd qjfr
$ ls
53013 mgrdrbl.lqg
191236 sgmnjc
$ cd ..
$ cd ..
$ cd zgczmvng
$ ls
260649 dglqpjs
141213 mgrdrbl.lqg
$ cd ..
$ cd ..
$ cd ..
$ cd vqrpdwv
$ ls
dir ftw
150895 mgrdrbl.lqg
227641 nbrzfl.dpf
dir nwjdnpdd
$ cd ftw
$ ls
99672 dbsgvvbp
dir dnzld
146730 mgrdrbl.lqg
$ cd dnzld
$ ls
37598 bhjbfl.svw
dir qspsslt
$ cd qspsslt
$ ls
dir vhgpwvf
$ cd vhgpwvf
$ ls
146936 ghgl
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd nwjdnpdd
$ ls
46000 trttdw.jsn
$ cd ..
$ cd ..
$ cd wpgddhdq
$ ls
dir rqgf
$ cd rqgf
$ ls
197374 rlvcvj.fmr
$ cd ..
$ cd ..
$ cd wpgv
$ ls
dir fdh
286086 fpwznlp.zsf
dir pljq
258062 wqvv
dir zgczmvng
$ cd fdh
$ ls
76173 fpwznlp.zsf
230947 nczhtpcn
62630 rlvcvj
$ cd ..
$ cd pljq
$ ls
dir mzmm
41117 rjms.dcg
$ cd mzmm
$ ls
144202 zgczmvng.ttl
$ cd ..
$ cd ..
$ cd zgczmvng
$ ls
dir dncr
dir mcdmfdp
dir pgqglmj
dir qldrmn
$ cd dncr
$ ls
198052 dcgbjvj
dir dqdgft
dir hpmwvnsr
2829 rlvcvj.qwg
$ cd dqdgft
$ ls
dir fng
dir nlsmb
$ cd fng
$ ls
198899 zgczmvng
$ cd ..
$ cd nlsmb
$ ls
257121 gmr.vmg
9276 zsmd.bng
$ cd ..
$ cd ..
$ cd hpmwvnsr
$ ls
241101 jjwqbwl.fpl
64151 wqvv
196139 zgczmvng
$ cd ..
$ cd ..
$ cd mcdmfdp
$ ls
276856 lrgbhq
$ cd ..
$ cd pgqglmj
$ ls
36476 fpwznlp.zsf
$ cd ..
$ cd qldrmn
$ ls
295686 trttdw.jsn
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd ..
$ cd dcgbjvj
$ ls
dir brdfvd
dir crstpjjv
dir fzdqcgv
dir fzw
dir mrllpw
dir wnh
119561 zgczmvng.jsm
$ cd brdfvd
$ ls
272932 mhdjc.mng
dir wqvv
91053 zgczmvng.jwg
$ cd wqvv
$ ls
dir bpplph
121367 jhlqfn.sbs
61760 nsgbt
46653 sbf.vcc
16952 trttdw.jsn
$ cd bpplph
$ ls
1288 rlvcvj
$ cd ..
$ cd ..
$ cd ..
$ cd crstpjjv
$ ls
117722 sbf.vcc
$ cd ..
$ cd fzdqcgv
$ ls
289819 fpwznlp.zsf
$ cd ..
$ cd fzw
$ ls
dir dcgbjvj
dir zsfqwdth
dir zswdl
$ cd dcgbjvj
$ ls
272427 cnsb.cmm
$ cd ..
$ cd zsfqwdth
$ ls
dir bdbgtqjj
dir hcgrqbhl
$ cd bdbgtqjj
$ ls
318980 tnqmspdf.cwd
$ cd ..
$ cd hcgrqbhl
$ ls
135307 fpwznlp.zsf
dir wqvv
$ cd wqvv
$ ls
68708 ctz.wms
149578 wlvdrfsw.qcj
$ cd ..
$ cd ..
$ cd ..
$ cd zswdl
$ ls
259754 cnsb.cmm
$ cd ..
$ cd ..
$ cd mrllpw
$ ls
44007 tvsm
$ cd ..
$ cd wnh
$ ls
dir mjnrmb
156515 wpdhq.hvp
$ cd mjnrmb
$ ls
293592 fpwznlp.zsf
$ cd ..
$ cd ..
$ cd ..
$ cd nsgms
$ ls
dir dnhzj
dir ptc
dir tnfrr
dir vjt
32152 zgczmvng.wmt
$ cd dnhzj
$ ls
281195 flqbvrw.gmf
177042 jjsfrmc.drz
$ cd ..
$ cd ptc
$ ls
dir gjvnrcln
290797 pccmrnn
59802 rzl.tjm
dir zgczmvng
$ cd gjvnrcln
$ ls
dir jph
$ cd jph
$ ls
105648 hflqlwr.mph
158151 hmlqsp
$ cd ..
$ cd ..
$ cd zgczmvng
$ ls
3700 bwn.wqq
240004 jbvhs.chq
224969 mvftsj
$ cd ..
$ cd ..
$ cd tnfrr
$ ls
dir hlbrpt
237956 mgrdrbl.lqg
dir wqvv
$ cd hlbrpt
$ ls
34424 crstpjjv.rlw
dir dzs
275267 mwrvw
313095 nwqzrc.tnf
61808 wzhgm.fft
$ cd dzs
$ ls
274302 cbbvq.vvh
234166 dcgbjvj.cbq
253156 fpwznlp.zsf
7239 nzdbr
$ cd ..
$ cd ..
$ cd wqvv
$ ls
120918 hchsfcp.clm
105770 nfhrd.tts
$ cd ..
$ cd ..
$ cd vjt
$ ls
dir crstpjjv
$ cd crstpjjv
$ ls
81225 fpwznlp.zsf
$ cd ..
$ cd ..
$ cd ..
$ cd wqvv
$ ls
72054 bcld.nwh
284293 cvsmmh
32684 ndgnz
130836 rlvcvj
233437 sbf.vcc
dir szwnlv
$ cd szwnlv
$ ls
133507 bnmhmpr.vww
'''

P1_SAMPLE_SOLUTION = 95437

P2_SAMPLE_SOLUTION = 24933642

class Directory():
    def __init__(self,name,parent=None):
        self.name = name
        self.parent = parent
        self.files = {}
        self.subdirs = {}
        self.pwd = None
        self.size = 0

class File():
    def __init__(self,name,parent,size=0):
        self.name = name
        self.parent = parent
        self.size = int(size)

class Puzzle():
    def __init__(self,input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split('\n')
        self.root = Directory("/")
        self.directories = []
        self.files = []
        self.pwd = self.root
                
    def process_terminal_history(self):
        self.instructions = []
        
        for line in [line.split() for line in self.input_list]:
            if line[0:2] == ["$","cd"]:
                if line[2] == "/":
                    self.pwd = self.root
                elif line[2] == "..":
                    self.pwd = self.pwd.parent
                else:
                    self.pwd = self.pwd.subdirs[line[2]]
            elif line[0] == "dir":
                self.pwd.subdirs[line[1]] = Directory(name=line[1],parent=self.pwd)
                self.directories.append(self.pwd.subdirs[line[1]])
            elif line[0].isnumeric():
                self.pwd.files[line[1]] = File(name=line[1],parent=self.pwd,size=int(line[0]))
                self.files.append(self.pwd.files[line[1]])
                self.pwd.size += int(line[0])
                size_updater = self.pwd.parent
                while size_updater != None:
                    size_updater.size += int(line[0])
                    size_updater = size_updater.parent
    
    def p1(self):
        self.process_terminal_history()
        self.p1_solution = 0
        for directory in self.directories:
            if directory.size <= 100000:
                self.p1_solution += directory.size
        
        return True

    def p2(self):
        total_disk_space = 70000000
        free_disk_space = total_disk_space - self.root.size
        required_unused_space = 30000000
        self.p2_solution = min([ directory.size for directory in self.directories if free_disk_space + directory.size >= ( required_unused_space) ])
        
        return True
            

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

def main():
    parser = argparse.ArgumentParser(description=f'AOC2022 Puzzle Day { DAY }')
    parser.add_argument("-p", "--showpuzzle", help="Display Puzzle Text", action='store_true')
    parser.add_argument("-s", "--showsample", help="Display Sample Input", action='store_true')
    args = parser.parse_args()
    
    if args.showpuzzle:
        print(f"###############\nAOC 2022 DAY {DAY} PUZZLE TEXT\n###############")
        print(PUZZLE_TEXT)
    
    if args.showsample:
        print(f"###############\nAOC 2022 DAY {DAY} SAMPLE INPUT\n###############")
        print(SAMPLE_INPUT.strip())
        print(f"\n###############\nAOC 2022 DAY {DAY} P1 SAMPLE SOLUTION\n###############")
        print(P1_SAMPLE_SOLUTION)
        print(f"\n###############\nAOC 2022 DAY {DAY} P2 SAMPLE SOLUTION\n###############")
        print(P2_SAMPLE_SOLUTION)
    

    if P1_SAMPLE_SOLUTION:
        print("PART 1\nRunning Sample...\n")
        start_time = time()
        sample = Puzzle(input_text=SAMPLE_INPUT)
        sample.p1()
        if P1_SAMPLE_SOLUTION == sample.p1_solution:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P1_SAMPLE_SOLUTION}, got {sample.p1_solution}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            puzzle = Puzzle(input_text=PUZZLE_INPUT)
            puzzle.p1()
            print("Running Input...\n")
            start_time = time()
            print(f'SOLUTION: {puzzle.p1_solution}')
            print(f"Elapsed time {elapsed_time(start_time)}")

    if P2_SAMPLE_SOLUTION:
        print("PART 2\nRunning Sample...\n")
        start_time = time()
        sample.p2()
        if P2_SAMPLE_SOLUTION == sample.p2_solution:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P2_SAMPLE_SOLUTION}, got {sample.p2_solution}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            print("Running Input...\n")
            puzzle.p2()
            start_time = time()
            print(f'SOLUTION: {puzzle.p2_solution}')
            print(f"Elapsed time {elapsed_time(start_time)}")
            
if __name__ == "__main__":
    main()