BEGIN
  ORDS_ADMIN.ENABLE_OBJECT(
    p_schema => 'admin',
    p_object => 'MUSEUMS',
    p_object_type => 'TABLE'
  );

  ORDS_ADMIN.ENABLE_OBJECT(
    p_schema => 'admin',
    p_object => 'PRODUCTS',
    p_object_type => 'TABLE'
  );  
  COMMIT;
END;