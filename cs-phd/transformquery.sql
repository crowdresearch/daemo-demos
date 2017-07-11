SELECT Name, Surname, Degree.Degree, Education.EndYear, SUM(professor)>0 as is_professor, SUM(startup)>0 as is_entrepeneur, SUM(scientist)>0 as is_scientist, SUM(engineer)>0 as is_engineer
FROM Person, Experience, Company, Education, Degree,
  (SELECT Title.TitleId, Title.Title,

  ((Title.Title LIKE '%professor%' OR Title.Title LIKE '%faculty%' OR Title.Title LIKE '%instructor%' OR Title.Title LIKE '%lecturer%' OR Title.Title LIKE '%dean%')
  AND Title.Title NOT LIKE '%visiting%' AND Title.Title NOT LIKE '%acting%' AND Title.Title NOT LIKE '%consulting%' AND Title.Title NOT LIKE '%adjunct%') AS professor,

  (Title.Title LIKE '%founder%' OR Title.Title LIKE '%owner%' OR Title.Title
  LIKE '%partner%' OR Title.Title
  LIKE '%\bCEO\b%' OR Title.Title
  LIKE '%\bCTO\b%') AS startup,

  ((Title.Title LIKE '%researcher%' OR Title.Title LIKE '%scientist%' OR Title.Title LIKE '%\bMTS\b%' OR Title.Title LIKE '%technical staff%' OR Title.Title LIKE '%research staff%')) AND Title.Title NOT LIKE '%visiting%' AS scientist,

  (Title.Title LIKE '%programmer%' OR Title.Title LIKE '%architect%' OR Title.Title LIKE '%engineer%' OR Title.Title LIKE '%engineering%' OR Title.Title LIKE '%designer%' OR Title.Title LIKE '%technologist%' OR Title.Title LIKE '%developer%') AS engineer

  FROM Title

  WHERE Title.Title NOT LIKE '%graduate%' AND Title.Title NOT LIKE '%intern%' AND Title.Title NOT LIKE '%ph(\.)?d(\.)?%' AND Title.Title NOT LIKE '%post(-)?doc(toral)?%') AS TitleType

WHERE Person.PersonId = Experience.PersonID AND Experience.CompanyID = Company.CompanyId AND Experience.TitleId = TitleType.TitleID AND Education.PersonID = Person.PersonID And Education.DegreeId = Degree.DegreeId AND Degree.Degree LIKE '%ph%d%'

GROUP BY Person.PersonId ORDER BY Person.Name;
