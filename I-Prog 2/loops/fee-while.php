<?php
// fee-while.php - Calculates expected fees for the next seven consecutive semesters using a while-loop.

$fee1 = null;
$fees = [];
$error = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $fee1_raw = $_POST['fee1'] ?? null;
  if ($fee1_raw === null || $fee1_raw === '' || !is_numeric($fee1_raw)) {
    $error = 'Please enter a valid number for Semester 1 fee.';
  } else {
    $fee1 = (float)$fee1_raw;
    if ($fee1 < 0) {
      $error = 'Fee must be a non-negative number.';
    } else {
      $increment = 1500;

      $i = 1; // to compute Semester 2..Semester 8 (7 semesters)
      while ($i <= 7) {
        $semesterNumber = 1 + $i; // 2..8
        $fees[] = [
          'semester' => $semesterNumber,
          'amount' => $fee1 + ($i * $increment)
        ];
        $i++;
      }
    }
  }
}

function h($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Fee Increment Result - While Loop</title>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;background:#f6f7fb;margin:0;padding:24px;}
    .card{max-width:720px;background:#fff;border-radius:10px;padding:18px 18px;box-shadow:0 8px 20px rgba(0,0,0,.06)}
    .error{background:#ffe8e8;border:1px solid #ffb3b3;color:#842029;padding:10px;border-radius:8px;}
    table{width:100%;border-collapse:collapse;margin-top:14px}
    th,td{border:1px solid #e6e6e6;padding:10px;text-align:left}
    th{background:#f1f3ff}
    .btn{display:inline-block;margin-top:14px;padding:10px 14px;border-radius:8px;background:#0b5ed7;color:#fff;text-decoration:none}
  </style>
</head>
<body>
  <div class="card">
    <h2>Fee Increment Result (While Loop)</h2>

    <?php if ($error): ?>
      <div class="error"><?php echo h($error); ?></div>
    <?php else: ?>
      <?php if ($fee1 !== null): ?>
        <p>Semester 1 fee entered: <strong>Ksh <?php echo number_format($fee1, 2); ?></strong></p>
        <p>Increment per semester: <strong>Ksh 1500</strong></p>

        <table>
          <thead>
            <tr><th>Semester</th><th>Expected Fee (Ksh)</th></tr>
          </thead>
          <tbody>
            <?php foreach ($fees as $row): ?>
              <tr>
                <td>Semester <?php echo h($row['semester']); ?></td>
                <td><?php echo number_format($row['amount'], 2); ?></td>
              </tr>
            <?php endforeach; ?>
          </tbody>
        </table>
      <?php else: ?>
        <p>Submit the form to see the computed fees.</p>
      <?php endif; ?>
    <?php endif; ?>

    <a class="btn" href="fee-while.html">Back</a>
  </div>
</body>
</html>

