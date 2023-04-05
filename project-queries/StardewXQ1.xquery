let $LocXML := collection('xmlfiles/LocationsXML/?select=*.xml')
let $names := $LocXML//@who
let $text := $LocXML//dialogue
