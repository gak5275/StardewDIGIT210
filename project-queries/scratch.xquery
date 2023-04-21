declare variable $stardew := collection("allfiles/all");
(: CAUTION: ABOVE IS A RELATIVE FILE PATH DESIGNED FOR WORKING IN oXYGEN ON YOUR LOCAL COMPUTER.
IT READS UP ABOVE THE PARENT DIRECTORY OF THIS XQUERY FILE, and DOWN INTO FILES IT NEEDS IN A PROJECT.
:)

(:declare variable $colors := ("#4B158D", "#324376", "#50B65E", "#586BA4", "#F5DD90", "#2564EE", "#F68E5F", "#F76C5E", "#AF9AB2", "#FED839", "#820B8A", "#672A4E", "#5CF64A", "#43B929", "#FF37A6", "#0DAB76", "#0B5D1E", "#191716", "#440D0F", "#84596B", "#758ECD", "#A0DDFF", "#0D5C63", "#FF6978", "#dc2f02");:)
(: declare variable $colors := ("#264653", "#264653", "#286569", "#297574", "#29817c", "#2a9187", "#2a9d8f", "#49a389", "#6fab82", "#93b27b", "#adb876", "#c8bd71", "#e9c46a", "#ebbf69", "#ecbb68", "#edb767", "#efb165", "#f1aa63", "#f4a261", "#f29c5f", "#f0965d", "#ee8f5b", "#ed8a59", "#eb8156", "#e76f51"); :)
(: declare variable $colors := ("#264653", "#6fab82"); :)

declare variable $xSpacer := 5;
declare variable $ySpacer := 50;

(: These are the different kinds of name types to look for :)


declare variable $allNames := $stardew//dialogue/@who => distinct-values() => sort();
declare variable $name-colors := 
    for $a at $pos in $allNames
        let $color := ('(' || 0 || ',' || $pos * 3 || ',' || $pos* 7 || ')')
        return ($a || '-rgb' || $color);
        

declare variable $namesSortedByCounts := 
    for $n in $allNames
            let $countType := $stardew//Q{}dialogue[@who = $n]/@who => count()
            order by $countType descending
            return $n;
$name-by-counts