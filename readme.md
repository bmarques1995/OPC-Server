# Servidor OPC #

Para rodar o servidor OPC, abra os seguintes programas, respectivamente:

`tanque.py`
`CLP.py`
`cliente_tcp.py`

Onde o `tanque.py` é independente, `CLP.py` depende de `tanque.py` e `cliente_tcp.py` depende de `CLP.py`.

O Programa se encerra ao receber um valor de nível menor que .05(5%) ou maior que .95(95%)