let $StardewColl := collection('../python/Target/autotag/?select=*.xml')
(: ?select=*.xml : We need this because your local file systems have hidden system files in your directory
that will interfere with XQuery:)

let $who := $StardewColl//dialogue/@who ! lower-case(.) ! normalize-space() => distinct-values()
let $names := $StardewColl//name ! lower-case(.) ! normalize-space() => distinct-values()

    
    let $whoConcat := for $s in $who
                               let $locations := $StardewColl[//location/@place ! normalize-space() = $s]
                               for $l in $locations
                                    let $lCode := $l ! base-uri() ! tokenize(., '/')[last()] ! substring-before(., '.xml')
                                    let $concat := ($s || "&#x9;" || "PERSON" || "&#x9;"|| $lCode || "&#x9;" || "location")
                                    return $concat => distinct-values()
                               
   (:  ebb: I get Java Heap space problem processing these in oXygen, so commenting out for now :)
   let $namesConcat := for $n in $names 
                                 let $locations := $StardewColl[.//name ! normalize-space() = $n]
                                 let $type := "PERSON"
                                 for $l in $locations
                                    let $lCode := $l ! base-uri() ! tokenize(., '/')[last()] ! substring-before(., '.xml')
                                    let $concat := ($n || "&#x9;" || $type || "&#x9;" || $lCode || "&#x9;" || "location")
                                    return $concat => distinct-values() 
                                    
                                 
                                    
                                    
   let $allRows := ($whoConcat, $namesConcat)
   
   let $string-join := string-join($allRows,  "&#10;")
   return $string-join