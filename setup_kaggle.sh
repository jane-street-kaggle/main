kaggle competitions download -c jane-street-real-time-market-data-forecasting
unzip jane-street-real-time-market-data-forecasting.zip 'kaggle_evaluation/*'
mkdir -p /kaggle/input/jane-street-realtime-marketdata-forecasting
unzip jane-street-real-time-market-data-forecasting.zip -d /kaggle/input/jane-street-realtime-marketdata-forecasting
rm -rf jane-street-real-time-market-data-forecasting.zip  