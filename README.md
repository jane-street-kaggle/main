# main
```
kaggle datasets create -p import-rtdl_revisting_models
kaggle datasets create -p import-rtdl_num_embeddings

!pip install rtdl_revisiting_models --no-index --find-links=file:///kaggle/input/js-rtdl-models
!pip install rtdl_num_embeddings --no-index --find-links=file:///kaggle/input/js-rtdl-embeddings

scp -r ~/.kaggle vastai1:~/.kaggle
scp ~/.ssh/enigma_ssh_key_rsa vastai1:~/.ssh/enigma_ssh_key_rsa
```