xquery version "3.1";
(: start by declaring global variables. These must end with a semicolon ;  :)
declare variable $xSpacer := 5;
declare variable $ySpacer := 20;
declare variable $colors := ("red", "green", "blue", "orange", "black", "purple", "aqua");
declare variable $Stardew1 := collection('autotag/North');
declare variable $Stardew2 := collection('autotag/South');
declare variable $Stardew3 := collection('autotag/East');
declare variable $Stardew4 := collection('autotag/West');
declare variable $StardewAll := ($Stardew1, $Stardew2, $Stardew3, $Stardew4);
(: In oXygen, adjust the filepath and use ?select=*.xml at the end to read around your schema and computer system files.:)
declare variable $allCatches := $StardewAll//name => distinct-values();
declare variable $distCatches := $StardewAll//name ! normalize-space() ! lower-case(.) ! replace(., "'", '') => distinct-values();

<svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
    <g transform="translate(50, 20)">
    <!--Use XML comments down here in the XML plot. In SVG, transform/translate shifts things by X and Y coordinates.
    So this moves the whole plot over by 50 and down by 20 from top left. We're going to start by plotting down the screen.
    We can come back here to work on flipping the plot in a different direction.
    Here's a lot more you can do with the transform attribute in SVG: 
    https://jenkov.com/tutorials/svg/svg-transformation.html 
    
    Okay, let's take a look at the catchphrases across the season! 
    -->
    {for $d at $pos in $distCatches 
    let $countThisCatch := $StardewAll//Q{}name[normalize-space() ! lower-case(.) ! replace(., "'", '') = $d] => count()
    (: The Q{} lets us dodge the SVG namespace that now dominates the field. It means qualified or local name :)

(: $pos is a number that counts each time the for statement runs. 
 : It should generate numbers 1 through 7 and we can use that for spacing. :)

(: We can start by plotting down the screen from top left. 
 : So we'll move y regularly down the screen using the $pos variable and the $ySpacer.  :)

return 
    <g id="{$d}">
        
        <line x1 = '{0}' y1 ='{$pos * $ySpacer}'  x2= '{$xSpacer * $countThisCatch}' y2="{$pos * $ySpacer}" stroke='{$colors[position() = $pos]}' stroke-width='5'/>
        
    
    </g>
}

</g>
</svg>