BEGIN
  ORDS_ADMIN.ENABLE_OBJECT(
    p_schema => 'admin',
    p_object=>'MUSEUMS'
  );

  ORDS_ADMIN.ENABLE_OBJECT(
    p_schema => 'admin',
    p_object=>'PRODUCTS'
  );  
  COMMIT;
END;