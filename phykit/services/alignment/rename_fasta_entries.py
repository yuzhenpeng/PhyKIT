from Bio import SeqIO

from .base import Alignment

class RenameFastaEntries(Alignment):
    def __init__(self, args) -> None:
        super().__init__(**self.process_args(args))

    def run(self):
        # create biopython object of sequences
        records = SeqIO.parse(self.fasta, "fasta")

        # save idmap to a dictionary
        idmap = self.idmap_to_dictionary(self.idmap)

        # replace and write out
        self.replace_ids_and_write(self.output_file_path, records, idmap)

        
    def process_args(self, args):
        return dict(
            fasta=args.fasta, 
            idmap=args.idmap,
            output_file_path=f"{args.fasta}.renamed.fa"
        )

    def replace_ids_and_write(self, output_file_path, records, idmap):
        """
        for tips with a name as a key in the idmap,
        replace that tip name with the value in the
        idmap and write to output file
        """
        with open(output_file_path, 'w') as output_file_path:
            for record in records:
                if record.id in idmap:
                    # replace ID
                    record.id = idmap[record.id]
                    # remove description
                    record.description = ''
                SeqIO.write(record, output_file_path, "fasta")

    def idmap_to_dictionary(self, idmap:str) -> dict:
        """
        read idmap into a dictionary
        """
        idmap={}
        with open(self.idmap) as identifiers:
            for line in identifiers:
                (key, val) = line.split()
                idmap[key] = val
        return idmap
