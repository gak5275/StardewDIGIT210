let $LocXML := collection('../python/Target/autotag/?select=*.xml')
let $text1 := $LocXML//dialogue
let $names := $text1/@who ! string()
let $text2 := $LocXML//name[@type='PERSON'] ! string() ! normalize-space() => distinct-values()
let $locations := $LocXML//location/@place ! string() ! normalize-space() => distinct-values()
let $concat := ($text2 || "&#x9;" || "PERSON" || "&#x9;" || $locations || "&#x9;" || "location")
let $stringjoin := string-join($concat,  "&#10;")

return ($text2 || "&#x9;" || "PERSON" || "&#x9;" || $locations || "&#x9;" || "location" || "&#10;") => distinct-values()