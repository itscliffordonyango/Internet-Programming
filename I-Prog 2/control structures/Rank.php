<?php
// Rank the ages of students in a class.
// Example input:
// Ages: [18, 20, 19, 20]
// Output ranks: [2, 0, 1, 0] (0 = highest)

$ages = [18, 20, 19, 20];

// Rank logic:
// - Higher age => better rank (smaller rank number)
// - Equal ages share the same rank

$uniqueAgesDesc = array_values(array_unique($ages));
rsort($uniqueAgesDesc); // sort ages descending

$ageToRank = [];
foreach ($uniqueAgesDesc as $i => $age) {
    $ageToRank[$age] = $i;
}

$ranks = array_map(function ($age) use ($ageToRank) {
    return $ageToRank[$age];
}, $ages);

// Output
header('Content-Type: text/plain; charset=utf-8');

echo "Student Ages and Ranks\n";
echo "-----------------------\n";

for ($i = 0; $i < count($ages); $i++) {
    $studentNo = $i + 1;
    $rankHuman = $ranks[$i] + 1; // make 1-based for display
    echo "Student {$studentNo}: Age={$ages[$i]} -> Rank={$rankHuman}\n";
}

