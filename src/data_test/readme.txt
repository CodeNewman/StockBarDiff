
Symbol A
// 20170821184610
// https://54.223.238.148:8443/cn/quote/symbols?&type=1&token=6fab4b8e8bd63ccd37d1a5130a32659e


Symbol B
// 20170821180250
// https://54.223.238.148:8443/cn/quote/prices/daily?symbols=600000&period=10&token=6fab4b8e8bd63ccd37d1a5130a32659e


symbol C
// 20170825115823
// http://121.43.168.179:8087/quote/prices/daily?symbols=ETW,AAPL&period=1

symbol D
// 20170825135853
// http://121.43.168.179:8087/quote/symbols/nyseandnasdaq
返回NYSE和NASDAQ的Symbols，数据来源Xiginte:
请求URL：
- /quote/symbols/nyseandnasdaq

请求方式：
- GET

返回字段说明:

参数名	类型	说明
status	number	接口返回状态，0为成功，非0为失败，失败信息在data中
data	string[]	响应信息，返回对应的symbol列表