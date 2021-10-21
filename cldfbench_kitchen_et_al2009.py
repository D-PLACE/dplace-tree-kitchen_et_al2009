import pathlib

import phlorest


class Dataset(phlorest.Dataset):
    dir = pathlib.Path(__file__).parent
    id = "kitchen_et_al2009"

    def cmd_makecldf(self, args):
        """
summary.trees: original/kitchen2009.mcct.trees
	nexus trees -c -t $< -o $@

posterior.trees: original/Semitic.Greenhill.trees.gz
	nexus trees -c -d 1-200 $< -o tmp
	nexus trees -n 1000 tmp -o $@
	rm tmp

data.nex:
	cp original/kitchen_et_al2009-Binary.nex $@
        """
        self.init(args)
        with self.nexus_summary() as nex:
            self.add_tree_from_nexus(
                args,
                self.raw_dir / 'kitchen2009.mcct.trees',
                nex,
                'summary',
                detranslate=True,
            )
        posterior = self.sample(
            self.remove_burnin(
                self.read_gzipped_text(self.raw_dir / 'Semitic.Greenhill.trees.gz'), 200),
            detranslate=True,
            as_nexus=True)

        with self.nexus_posterior() as nex:
            for i, tree in enumerate(posterior.trees.trees, start=1):
                self.add_tree(args, tree, nex, 'posterior-{}'.format(i))

        self.add_data(args, self.raw_dir / 'kitchen_et_al2009-Binary.nex')
