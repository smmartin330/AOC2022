import argparse
from time import time

DAY = 6

PUZZLE_TEXT = '''
--- Day 6: Tuning Trouble ---
--- Part One ---

The preparations are finally complete; you and the Elves leave camp on foot and begin to make your way toward the 
star fruit grove.

As you move through the dense undergrowth, one of the Elves gives you a handheld device. He says that it has many 
fancy features, but the most important one to set up right now is the communication system.

However, because he's heard you have significant experience dealing with signal-based systems, he convinced the 
other Elves that it would be okay to give you their one malfunctioning device - surely you'll have no problem fixing 
it.

As if inspired by comedic timing, the device emits a few colorful sparks.

To be able to communicate with the Elves, the device needs to lock on to their signal. The signal is a series of 
seemingly-random characters that the device receives one at a time.

To fix the communication system, you need to add a subroutine to the device that detects a start-of-packet marker 
in the datastream. In the protocol being used by the Elves, the start of a packet is indicated by a sequence of four characters that are all different.

The device will send your subroutine a datastream buffer (your puzzle input); your subroutine needs to identify 
the first position where the four most recently received characters were all different. Specifically, it needs to 
report the number of characters from the beginning of the buffer to the end of the first such four-character marker.

For example, suppose you receive the following datastream buffer:

mjqjpqmgbljsphdztnvjfqwrcgsmlb

After the first three characters (mjq) have been received, there haven't been enough characters received yet to
find the marker. The first time a marker could occur is after the fourth character is received, making the most 
recent four characters mjqj. Because j is repeated, this isn't a marker.

The first time a marker appears is after the seventh character arrives. Once it does, the last four characters 
received are jpqm, which are all different. In this case, your subroutine should report the value 7, because the 
first start-of-packet marker is complete after 7 characters have been processed.

Here are a few more examples:

bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 5
nppdvjthqldpwncqszvftbrmjlhg: first marker after character 6
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 10
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 11
How many characters need to be processed before the first start-of-packet marker is detected?

--- Part Two ---

Your device's communication system is correctly detecting packets, but still isn't working. It looks like it also needs to look for messages.

A start-of-message marker is just like a start-of-packet marker, except it consists of 14 distinct characters rather than 4.

Here are the first positions of start-of-message markers for all of the above examples:

mjqjpqmgbljsphdztnvjfqwrcgsmlb: first marker after character 19
bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 23
nppdvjthqldpwncqszvftbrmjlhg: first marker after character 23
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 29
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 26

How many characters need to be processed before the first start-of-message marker is detected?
'''

SAMPLE_INPUT = '''
mjqjpqmgbljsphdztnvjfqwrcgsmlb
'''

PUZZLE_INPUT = '''
sgrrrrwcrrlqqgppfgfnngsgcgngrrllnqnndzzjgzzzjdjqdjdhhjshjhwwqnnwjnwnjwjttvgvddjrrtvtsvtvqtqhhbchcdhhnwwvqvvsbsqswqqdwdjwwjvvrddgpdpdlpljjwffqnffbllplmmwzwtzzvfzvvjbbmnmppzgzszllsqqpvqvmmzzlccjhchdhlddchdchcddnwdwhhhczzldlsdlssdmmswswzwtwzwjzwzfwwdhwdwjdjldjldlqddhttfbfnbfnfgnfnvnffsszjjsqqdzdsdrsswddggstgsgqgzqgqcqdccqcvcpcspccdgccfflppddqfdfmdffmlflplnppfvvgsgbgtgccmfccfwwthhcjcbbhbwbjbhjjtddrldlrddzjdzdttbfbmmtjmjtjzjvjvgvttthwhhgqhggcbbtqbbqgbqqvccdttfgfwfnwffbfqbfbbnlnzlzbbwnwntwtjwjnjwwsdwwcbbwhwzwhwvhhpwwnvvtvnttgtrrnjjzppmbmfmjffdddvfvjjpfpgpzzwqwpwllwjjzmjmdmdwwdrdttpmmdhdndvvpbpqbbzqzmmtdmmtddlccjvjsjrsscqqzvvbsstccvffcttwrwjjsgsttmgmvvzbbcjbjrbrddvjjnhjhphvhsszqqfrfzfssgfssgddcbbplbbsfsmfmpphssmvvcvrrcgrcgcvggrzggzjjfhjjtpphzppqtptllssbmbrrgrvvhjjnznlnggrnrsnrrphhbqhhhsthsthhhnssmsjjwjppqfqlqqgnnhnmmfsfslfllvnnsdnssgngbbjmjccsrrmjjnljlwlttpffddgbdggmbgbtbzzwgwppczcffvccnssbmmjrrfwwhcwhwqwnqqzsqqjsqqnndqdgqdqgggzjjcvvzdddhnhjnnzlnlwlzlqqvjjpprqrjrfjjrpjjnfntffqtttnjjdbjbdjbbrsrbbmrmccpllmccqrqwqnnsjjmjgjqjpqjqgjjtwwqdqmqtqqmsqmmvlldtllbcctfcccdcddcggmmmsggjddcqddbqqdgqgffststgtftbbdrbrlllnvllcflfpfdffjvvvmdmvvtfvfcvvfgghzzlgzgszzhmzzhfhllgblggfpfzfvzvdzzhsspmmjtjhjggfhggnggbtggqqtztqtmqtqddmzmrmdrmdmqqcbqcqzzvczvzfvvsggcgssjnnjqnntwtmwwhzzzhllqvlljsljjfnnjwjnwnffpggqwwvbwwdbbmbvmvlvnnnppqvqqghqgqppnllhjllvlflfpfhfjjhgjgpjpbjjdpdqdpqdpdwpwffqlffrbrjrtrvtvrtvrtrvtvltlrrvjjlttmtffhvfhfnhnlnfnvvltvlvlbbfllfnllndndcdrrnznssvpvhhhmrmlmhhrnhhpggtftddghhqrqddjttbdbqddpsdppwrwhhhgwhhqrhqrqhhqdhqddjpjqqsdsmddnqncqnqwqdwwhghbhffnsffnsszlssntnbbbfhbhwhzhdzhzbhblbzzzbqzbbgtbbcjbjtjptpwwhlwwhhmshhmbbfjbfflnnlmnnzvnnbtnbbvwvvgcggrzrffwmwhmwhwjwpwwzbbvtbtssdhdlhhdppmmcnmcmffnpfffvbfvfhvhjhffzfbzzfdfpdpzzhbzblbbmffvvcmmttdntnmtmztzbbncbctcqtcqqcvcfcwcdcchphfhjhhjbjnjtjnjwwzsstpprnnhtntvtpthpttpdpzzwcczsscqscsbbmpbbdsdlsslzszjszsczntrqjmmmfqsdwtqqflgsttwfqqvvspnlfvqlrvvbjmmpmttcdnhncmmdfhwwqdrqjqwggrbtgbrdmmrhhvqfvvhsmtfbnthrbltgvdrsbqglgjqtssbvmbjjjbbcgfftgbjmfqzggdtcfzddqlrvwqjjvnmjzjwqrwsqbjgnswpnlbdzdlcvcbqplzgqwmsntzzjhqwfjdprglcccnldfqftgttqbrmclsqtncrjbttcglcvspsgvdjqgrdzzlnhbfqbwnfqcjrrqpprjbqpzhthgsgcflqldsnwsvzgcmfrdvfmqhbcfczhschpwnmdjnjlvrwqllnnhjvjtzhcrqcwlmrqfdhvzcbnvwrgngttwlhcmmgtzwjztscjnmslbvtdrvgdprlfrhggcwtwjhblppfbpljbmwrlwqrfwjwfsftmflsdfrhlvgcbzcvhlhgclvnmtfcqttvcphgvflhdclbmtgsrldgfvtpjcphtzdctrcchwdbdbtpptdnbjnqwdrllmnbcgfltmggpqfbfpmnhcmpgsgptflglzswtmrjfzmwmwphfjngnfmmtqlrsltlvlfmwmjvvtgngllszwzdjjmbnwwgzpqltlrzfdwchgttvlhgjjhjqmlrrwsqlhsgzsgmmsgbgvrlmbprrhlgsjnsdwcbrwvqjqmfcqcwllsvggcznwpzvgpszrqwngcnchvdlrdrgtbsjdqfpsfvwdtdlqwbfjlwrmqbrhwqmfgppwvfbgthnbqnmqqhmpfwbgljcmqqbpnwvztrcrlbvtcnncwwjcbqsmbqnqtrmpwmhlvwtfmsmtpfnmphqdvqfzvmjjhnwdfjnwvmbbwvthhwzjtzzrsmqlqtnnrqjrnchqttgsptfpdcpgfmzvqhwffqmfhwqqbdhmgcrfqtwrcgtgmglmmwhvqwvglfsvwbpvhmnbqhgfgqwwnhdhvnwggsmhjfsjmsrlcvlnhrhrlhbvhdrhbplrzspdmbcnzbwlvcmztwvghlsnzmbnrpssrngpdtmgzfcbqmfdgthcscjspspmcgdmwwwfspgjwzccrfzdpbwrfpgpgzrchffmhvwwppbjwqmdzgtpfmcblzqrghzdbzqzvbnmqbdlzjrwbbhqgtdzntgdbndmndhlnhcvqtlfcrfprfrlfglwvdnszrwjdcmtstcsnvnpcldctvqpcfhjnpvscscrtfqfjcrjlrmcqjfthptbqprbvchjlqzmfcmlhmfmdhhpcqbncmcqjsdmzflwtzfdcgmrbwbcdgjmfhlshsbwmbdcbfbvmqcgwlqpprjfrhzvsjmcjdfnwhcffhtnqpznfzpttsqqwcsvpdhdfbggzpngvbvdlpmvfjjlcfmbvmfqsczprtlnwvqnnlcrdnvpmcbrzvlfgscbcwtrbcpdnpshhmrqmhnwcndptljhwpvtcflqgmzjsfmfdzwwwhnbpzjwzgqmdcdbtfhwtgvcscbdqlcmppwjgghvrmqpwfbnjfhfcrccfzjvtjsjcsmhncdjlclvhfsvlcjcnpbqqqdjmjdbggmfwswvdjscvgrdbpcrcqtndswgdnznzpwtcdgvcrrqpdcpbmbdjrsgnfvgwpgpzttfmsczcmjvhmdpbpmjjcjsvbvbwjpwtwpsdddlsnvrshqvmwsjwwvqnczzljjfptcszgpndgczprbvjbnqpwgzmnlhvbsfbtjnwbtlzqgnmzbmqgqvwzltvqczfpdzfzsfhqlmtfcbfdqtnwzbvqblqmzvmnspntqtqdglrdmdntrghwvpfrbjgpzvrnppvnvfgwdzlvhtcscclbtftlvsprwhjvjlhrhfdgzbfbfphzbhtfdlpzcshhfzhtdvggnnbqvnrwvnhvgjgjpcrztqjmtzlzlrlmndfvctzjdpnmlgmsppqdrzmptvrsptvmmbvbwvhwptrtlfdqdqwfgldtbhqdhszcmwqnhswrdhgmgvbvbhwhlpcflsrwlvsvhvctmwwhtlgmshdqflwsdjbbzgbvbwpfncgqjzfjvmzzhgdzjvghtrtsmwgzpdrngwdbtfzrqsgdmwtdhsftfqcnmjtrqqwthcbgtmqnjvjzzplrzllnjqddvbwnglhtzljwjvscdfdnsvmrgwhjrhlrqpqgmzstnwwjpddhdbsnnsqvtsdhtmfdmbcpzwqmbhhjhcfzbvvglhfdltrmbstjhsqrbs
'''

P1_SAMPLE_SOLUTION = 7

P2_SAMPLE_SOLUTION = 19

def elapsed_time(start_time):
    return f"{round(time() - start_time, 4)}s\n"

def part_one(input_text=SAMPLE_INPUT):
    input_text = input_text.strip()
    for position in range(0,len(input_text)):
        group = {*input_text[position-4:position]}        
        if len(group) == 4:
            return position

def part_two(input_text=SAMPLE_INPUT):
    input_text = input_text.strip()
    for position in range(0,len(input_text)):
            group = {*input_text[position-14:position]}        
            if len(group) == 14:
                return position
        
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
        print("PART 1\nTesting Sample...\n")
        start_time = time()
        solution_output = part_one()
        if P1_SAMPLE_SOLUTION == solution_output:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P1_SAMPLE_SOLUTION}, got {solution_output}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            print("Processing Input...\n")
            start_time = time()
            print(f'SOLUTION: {part_one(PUZZLE_INPUT)}')
            print(f"Elapsed time {elapsed_time(start_time)}")
        
    if P2_SAMPLE_SOLUTION:
        print("PART 2\nTesting Sample...\n")
        start_time = time()
        solution_output = part_two()
        if P2_SAMPLE_SOLUTION == solution_output:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P2_SAMPLE_SOLUTION}, got {solution_output}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            print("Processing Input...\n")
            start_time = time()
            print(f'SOLUTION: {part_two(PUZZLE_INPUT)}')
            print(f"Elapsed time {elapsed_time(start_time)}")
    
if __name__ == "__main__":
    main()