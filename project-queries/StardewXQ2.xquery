let $StardewColl := collection('../python/Target/autotag/?select=*.xml')
(: ?select=*.xml : We need this because your local file systems have hidden system files in your directory
that will interfere with XQuery:)

let $who := $StardewColl//dialogue/@who ! normalize-space() => distinct-values()
let $names := $StardewColl//name[@type='PERSON'] ! normalize-space() => distinct-values()
(: let $location := $StardewColl//location/@place ! string() ! normalize-space()  => distinct-values() :)
    
    let $whoConcat := for $s in $who
                      let $files := $StardewColl[.//dialogue/@who ! normalize-space() = $s]
                      (: Above is your edge connector, the context for the linkage is the file :)
                     for $f in $files
                            let $fname := $f ! base-uri() ! tokenize(., '/')[last()]
                      
                               let $locations := $f[.//dialogue/@who ! normalize-space() = $s]//location/@place ! string() ! normalize-space()  => distinct-values()
                               
                               for $l in $locations
                                    (: let $lCode := $l ! base-uri() ! tokenize(., '/')[last()] ! substring-before(., '.xml') :)
                                    
                                    let $concat := ($s || "&#x9;" || "SPEAKER" || "&#x9;" || $fname ||"&#x9;"|| $l || "&#x9;" || "location")
                                    return $concat => distinct-values()
                               
   (:  ebb: I get Java Heap space problem processing these in oXygen, so commenting out for now :)
   let $namesConcat := for $n in $names 
                                 let $locations := $StardewColl[.//name ! normalize-space() = $n]
                                 let $type := "PERSON"
                                 for $l in $locations
                                    (: let $lCode := $l ! base-uri() ! tokenize(., '/')[last()] ! substring-before(., '.xml') :)
                                    let $location := $StardewColl//location/@place ! string() ! normalize-space()  => distinct-values()
                                    let $concat := ($n || "&#x9;" || $type || "&#x9;" || $location || "&#x9;" || "location")
                                    return $concat => distinct-values() 
                                    
                                 
                                    
                                    
   let $allRows := ($whoConcat)
   
   let $string-join := string-join($allRows,  "&#10;")
   return $string-join