jbsub -cores 1+1 -interactive -err err/e$1.txt -out out/o$1.txt -mem 150g -q x86_24h python run_train.py --load_checkpoint_path $1 --dump_checkpoint_path $1 --dump_data_path $1 --cluster_classify $2
