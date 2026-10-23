# Third-party provenance

The MIT license covers newly authored pilot code and documentation, not inputs, papers, solver libraries or inherited designs.

Hanoi network input and benchmark definitions: University of Exeter Centre for Water Systems, https://www.exeter.ac.uk/research/centres/cws/resources/benchmarks/ . Original problem attributed to Fujiwara and Khang (1990). Exeter offers these files for research; an explicit redistribution license has not yet been established. The public repository excludes the network input files; setup fetches them directly from Exeter and verifies their frozen hashes. The fetched Pareto-front file describes a different multiobjective task and is not used as a scalar cost record or as our comparator.

Published reference diameters were transcribed from Table8 of “Optimization of Water Distribution Networks Using Genetic Algorithm Based SOP–WDN Program”, Water14(6),851 (2022), DOI10.3390/w14060851, https://www.mdpi.com/2073-4441/14/6/851 . The article is published under CC BY4.0. Its PDF and extracted text are omitted from this public package; consult the original publication for attribution and license terms. The reference is not asserted to be the current global best. Exact formula costs differ from the paper's rounded price table.

WNTR1.5.0 is from https://github.com/USEPA/WNTR and carries its own revised BSD license; its packaged EPANET library and other dependencies retain their notices. Local source.zip from Exeter is kept only in ignored vendor/ for checking the objective definition; no upstream optimizer source is copied into our pilot code. Sources and hashes: research/sources.json.

Synthetic stress scenarios are authored for this qualification trial. They are not measurements or calibrated forecasts for a real network. No operational utility data was used.

Public packaging does not bundle externally sourced matrices, derived matrix archives, hydraulic network files, or downloaded reference-page/article snapshots. external-inputs.json records original sources and frozen hashes. Setup fetches the required inputs directly and reconstructs derived inputs without modifying the accepted scientific certificates. Original local research archives remain intact. Upstream terms govern downloaded inputs; the project MIT license does not replace them.
