A = load 'hdfs://namenode.europa.hadoop/user/ubuntu/customer_facts/customers_fact_log' as (id:int,customers_id:int,fact_type_id:int,date:chararray,attr1:chararray,attr2:chararray,attr3:chararray,attr4:chararray,attr5:chararray,attr6:chararray,attr7:chararray,attr8:chararray,attr9:chararray,attr10:chararray,attr11:chararray,attr12:chararray,attr13:chararray,attr14:chararray,attr15:chararray,attr16:chararray,attr17:chararray,attr18:chararray,attr19:chararray,attr20:chararray);

B = filter A by (fact_type_id == 23 and attr5 matches 'photo') or fact_type_id == 101651 or fact_type_id == 101652 or fact_type_id == 101653 or fact_type_id == 101654 or fact_type_id == 101662; 

C = order B by customers_id,date;

dump C;


