let $LocXML := collection('../xmlfiles/LocationsXML/?select=*.xml')
let $text := $LocXML//dialogue
let $names := $text/@who ! string()
let $Tnames := $LocXML//name/@type='PERSON'
return $Tnames