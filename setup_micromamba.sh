# >>> mamba initialize >>>
# !! Contents within this block are managed by 'micromamba shell init' !!
export MAMBA_EXE='/root/.local/bin/micromamba';
export MAMBA_ROOT_PREFIX='/root/micromamba';
__mamba_setup="$("$MAMBA_EXE" shell hook --shell bash --root-prefix "$MAMBA_ROOT_PREFIX" 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__mamba_setup"
else
    alias micromamba="$MAMBA_EXE"  # Fallback on help from micromamba activate
fi
unset __mamba_setup
# <<< mamba initialize <<<

micromamba create --name kaggle python=3.11 -c conda-forge -y
micromamba activate kaggle 
micromamba config append channels conda-forge
micromamba config append channels torch 
# linux-cuda 12.4
micromamba install pytorch torchvision torchaudio pytorch-cuda=12.4 -y -c pytorch -c nvidia 
micromamba install numpy=1.26.4 scikit-learn=1.5.2 boost lightning polars xgboost dill matplotlib optuna kaggle pandas pyarrow fastparquet catboost grpc-cpp -y -c conda-forge 