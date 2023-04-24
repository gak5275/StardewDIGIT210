declare variable $stardew := collection("allfiles/all");
(: CAUTION: ABOVE IS A RELATIVE FILE PATH DESIGNED FOR WORKING IN oXYGEN ON YOUR LOCAL COMPUTER.
IT READS UP ABOVE THE PARENT DIRECTORY OF THIS XQUERY FILE, and DOWN INTO FILES IT NEEDS IN A PROJECT.
:)

(:declare variable $colors := ("#4B158D", "#324376", "#50B65E", "#586BA4", "#F5DD90", "#2564EE", "#F68E5F", "#F76C5E", "#AF9AB2", "#FED839", "#820B8A", "#672A4E", "#5CF64A", "#43B929", "#FF37A6", "#0DAB76", "#0B5D1E", "#191716", "#440D0F", "#84596B", "#758ECD", "#A0DDFF", "#0D5C63", "#FF6978", "#dc2f02");:)
(: declare variable $colors := ("#264653", "#264653", "#286569", "#297574", "#29817c", "#2a9187", "#2a9d8f", "#49a389", "#6fab82", "#93b27b", "#adb876", "#c8bd71", "#e9c46a", "#ebbf69", "#ecbb68", "#edb767", "#efb165", "#f1aa63", "#f4a261", "#f29c5f", "#f0965d", "#ee8f5b", "#ed8a59", "#eb8156", "#e76f51"); :)
declare variable $colors := ("#d10017" (:Emily:), "#073b35" (:Harvey:), "#22629a" (:Shane:), "#5e011e" (:Elliott:), "#b7f3c8" (:Leah:), "#ffff96" (:Sam:), "#df433c" (:Penny:), "#7c44bf" (:Abigail:), "#fffc35" (:Haley:), "#391e47" (:Sebastian:), "#993e00" (:Alex:), "#9355ea" (:Lewis:), "#8e0154" (:Maru:), "#f77825" (:Robin:), "#000000" (:Universal:), "#f888c4" (:Pam:), "#110026" (:Krobus:), "#d16132" (:Pierre:), "#b76f4b" (:Leo:), "#8c0200" (:Willy:), "#1d66f2" (:Demetrius:), "#e34a16" (:Marnie:), "#db8200" (:Gus:), "#a0a0a0" (:Misc:), "#fee02a" (:Linus:), "#e75184" (:Jodi:), "#50b797" (:George:), "#c1ff7f" (:Caroline:), "#a0510c" (:Clint:), "#806fff" (:Wizard:), "#b6005b" (:Evelyn:), "#e4a0ff" (:Jas:), "#ffa39b" (:Vincent:), "#43551c" (:Kent:), "#5a5a7f" (:Morris:), "#b6b243" (:Snail:), "#8f8f46" (:Birdie:), "#d30a4d" (:Sandy:), "#3e2327" (:Dwarf:), "#37b230" (:Marlon:), "#42e8e3" (:Gunther:), "#c3fffa" (:Qi:), "#66ccff" (:Grandpa:), "#33cc33" (:Junimos:), "#996633" (:Bear:), "#333333" (:Bouncer:), "#660000" (:Gil:), "#9933cc" (:Governor:));
declare variable $xSpacer := 5;
declare variable $ySpacer := 50;

(: These are the different kinds of name types to look for :)


declare variable $allNames := $stardew//dialogue/@who => distinct-values();

declare variable $namesSortedByCounts := 
    for $n in $allNames
            let $countType := $stardew//Q{}dialogue[@who = $n]/@who => count()
            order by $countType descending
            return $n;
(: Count names to automatically determine marker sizes:)
declare variable $countallNames := $allNames => count();

declare variable $nameTotal := $stardew//dialogue/@who => count();
(: ebb: Note: The line above gets the count of all type attributes on names including duplicates. 
And yes, this is the value you want to use, and it works. We learn that 82% of the names are persons.
:)


(:I want to find how many distinct strings come up matching to each name Type :)




<svg
    width="100%"
    height="{($countallNames + 4) * $ySpacer}"
    xmlns="http://www.w3.org/2000/svg"
    overflow-y="scroll">
    
    <!-- Graph Markers -->
    <g
        transform="translate(150, 50)">
        <!-- X axis -->
        <line
            x1="0"
            y1="{($countallNames + 0.5) * $ySpacer}"
            x2="{100 * $xSpacer}"
            y2="{($countallNames + 0.5) * $ySpacer}"
            stroke="black"
            stroke-width="3"
        />
        <!-- Y axis -->
        <line
            x1="0"
            y1="{($countallNames + 0.5) * $ySpacer}"
            x2="0"
            y2="{0}"
            stroke="black"
            stroke-width="3"
        />
        <!-- Percentage Marks -->
        {
            for $i at $pos in (1 to 3)
            return 
                <line
                    x1="{33.333 * $pos * $xSpacer}"
                    y1="{0}"
                    x2="{33.333 * $pos * $xSpacer}"
                    y2="{($countallNames + 0.5) * $ySpacer}"
                    stroke="green"
                    stroke-width="1"
                ></line>
        }
        {
            for $i at $pos in (1 to 3)
            return
                <text
                    x = "{33.333 * $pos * $xSpacer}"
                    y = "{($countallNames + 1) * $ySpacer}">
                        {concat(round($pos * 33.333 div 6.666, 0), "%")}
                </text>
        }
    </g>
    
    
    <!-- Data -->
    <g
        transform="translate(150, 50)">
        
        
        {
            for $n at $pos in $namesSortedByCounts
            let $countType := $stardew//Q{}dialogue[@who = $n]/@who => count()
            
            
            let $namePerc := $countType div $nameTotal * 100
            (: Variable below to give scaled bars, but have accurate percentages (above):)
            let $nameScaled := $namePerc * 6.666 (:Final number limits graph size: 5 shows 20%, 10 shows 10%:)
            
            let $perc := $namePerc => format-number('01%')
            
            
            
            
            
            
            (: This is going to have it travel to the stardew collection, look for every name attribute and 
cycle through $n type for the attribute. Then it will travel to the attribute and count what kind of 
attribute it is. :)
            
            
            (: Look to output percentage type (Add everything up then divide it by how much it appears) :)
            
            
            return
                <g
                    id="{$n}">
                    
                    <line
                        x1='{0}'
                        y1='{$pos * $ySpacer}'
                        x2='{$nameScaled * $xSpacer}'
                        y2="{$pos * $ySpacer}"
                        stroke='{$colors[position() = $pos]}'
                        stroke-width='20'/>
                    
                    <text
                        x="-100"
                        y="{$pos * $ySpacer}"
                        stroke="black"
                    >
                        {$n}
                    
                    </text>
                    
                    <text
                        x="{$nameScaled * $xSpacer + 30}"
                        y="{$pos * $ySpacer}"
                        stroke="black"
                    >
                        {concat(round($namePerc, 3), "%")}
                    </text>
                
                
                </g>
        }
    
    
    </g>
</svg>