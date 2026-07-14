<?php
// Bookshop discount calculator , here I will use a  POST endpoint
// Inputs include: course_code (string/int), book_price (number)

function e(string $v): string {
    return htmlspecialchars($v, ENT_QUOTES, 'UTF-8');
}

$course_code_raw = $_POST['course_code'] ?? '';
$book_price_raw = $_POST['book_price'] ?? '';

$course_code = is_numeric($course_code_raw) ? (int)$course_code_raw : null;
$book_price = is_numeric($book_price_raw) ? (float)$book_price_raw : null;

if ($course_code === null || $book_price === null || $book_price < 0) {
    http_response_code(400);
    echo "Invalid input. Please provide a valid course code and a non-negative book price.";
    exit;
}

$course_name = "";
$discount_rate = 0.0;

// Determine course name and discount rate using switch-case
switch ($course_code) {
    case 101:
        $course_name = "Computer Science";
        $discount_rate = 0.15;
        break;
    case 202:
        $course_name = "Information Technology";
        $discount_rate = 0.12;
        break;
    case 303:
        $course_name = "Business Management";
        $discount_rate = 0.08;
        break;
    case 404:
        $course_name = "Engineering";
        $discount_rate = 0.10;
        break;
    case 505:
        $course_name = "Education";
        $discount_rate = 0.05;
        break;
    default:
        $course_name = "Unknown Course";
        $discount_rate = 0.0;
        break;
}

$discount_amount = $book_price * $discount_rate;
$amount_payable = $book_price - $discount_amount;

header('Content-Type: text/html; charset=utf-8');
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Switch Case Result</title>
  <style>
    body { font-family: Arial, Helvetica, sans-serif; background:#f6f7fb; padding:24px; }
    .card { max-width: 560px; margin: 0 auto; background:#fff; padding: 18px; border-radius: 10px; box-shadow: 0 6px 18px rgba(0,0,0,0.08); }
    h1 { font-size: 20px; margin: 0 0 10px; }
    .row { margin-top: 10px; font-size: 15px; }
    .btn { display:inline-block; margin-top: 16px; padding: 10px 14px; border-radius: 8px; background:#2563eb; color:#fff; text-decoration:none; font-weight:700; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Discount Result</h1>

    <div class="row"><strong>Course Name:</strong> <?php echo e($course_name); ?></div>
    <div class="row"><strong>Discount Rate:</strong> <?php echo number_format($discount_rate * 100, 2); ?>%</div>
    <div class="row"><strong>Discount Amount:</strong> $<?php echo number_format($discount_amount, 2); ?></div>
    <div class="row"><strong>Amount Payable:</strong> $<?php echo number_format($amount_payable, 2); ?></div>

    <a class="btn" href="bookshop.html">Calculate Again</a>
  </div>
</body>
</html>

