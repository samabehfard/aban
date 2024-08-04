### پروژه‌ی آبان تتر 

1. **ساخت ایمیج داکر**:

   ```bash
   docker compose build
   ```

2. **اجرای کانتینرها**:

   ```bash
   docker compose up
   ```

   این فرمان سرویس پایگاه داده PostgreSQL و سرور وب Django را راه‌اندازی می‌کند.

3. **اجرای مهاجرت‌ها**:

   مهاجرت‌ها را به پایگاه داده اعمال کنید:

   ```bash 
   docker exec -it aban python manage.py migrate     
   ```

### اجرای دستور ساخت کاربر تست

شما می‌توانید دستور `create_test_user` را به‌طور مستقل از داکر اجرا کنید:

```bash
docker exec -it aban python manage.py create_test_user <username> <usdt_balance>
```

**مثال**:

```bash
docker exec -it aban python manage.py create_test_user john 70
```

## استفاده از API

### 1. خرید ارز دیجیتال

- **آدرس**: `/api/purchase/`
- **روش**: POST
- **توضیحات**: به کاربر اجازه می‌دهد که در صورت داشتن موجودی کافی USDT، ارز دیجیتال خریداری کند.

**مثال درخواست**:

```bash
curl -X POST http://localhost:8000/api/purchase/ \
     -H "Content-Type: application/json" \
     -d '{
           "username": "john_doe",
           "currency_name": "BTC",
           "count": 2
         }'
```

**پاسخ مثال**:

- **موفقیت**:

  ```json
  {
    "message": "Purchase successful"
  }
  ```

- **خطاها**:

  - **کاربر پیدا نشد**:

    ```json
    {
      "error": "User not found"
    }
    ```

  - **موجودی کافی نیست**:

    ```json
    {
      "error": "Insufficient balance"
    }
    ```

  - **ارز دیجیتال پیدا نشد**:

    ```json
    {
      "error": "Cryptocurrency not found"
    }
    ```

### 2. مشاهده کیف پول‌های کاربر

- **آدرس**: `/api/wallets/<username>/`
- **روش**: GET
- **توضیحات**: دریافت همه کیف پول‌ها و موجودی آنها برای یک کاربر خاص.

**مثال درخواست**:

```bash
curl -X GET http://localhost:8000/api/wallets/john_doe/
```

**پاسخ مثال**:

- **موفقیت**:

  ```json
  [
    {
      "currency_name": "USDT",
      "amount": 100.50
    },
    {
      "currency_name": "BTC",
      "amount": 0.05
    }
  ]
  ```

- **کاربر پیدا نشد**:

  ```json
  {
    "error": "User not found"
  }
  ```
