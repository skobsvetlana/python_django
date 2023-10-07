select "shopapp_product"."id",
       "shopapp_product"."name",
       "shopapp_product"."description",
       "shopapp_product"."quantity",
       "shopapp_product"."price",
       "shopapp_product"."discount",
       "shopapp_product"."created_at",
       "shopapp_product"."created_by_id",
       "shopapp_product"."archived",
       "shopapp_product"."preview"
from "shopapp_product"
where not "shopapp_product"."archived"
order by "shopapp_product"."name" asc, "shopapp_product"."price" asc;


select "shopapp_product"."id",
       "shopapp_product"."name",
       "shopapp_product"."description",
       "shopapp_product"."quantity",
       "shopapp_product"."price",
       "shopapp_product"."discount",
       "shopapp_product"."created_at",
       "shopapp_product"."created_by_id",
       "shopapp_product"."archived",
       "shopapp_product"."preview"
from "shopapp_product"
where "shopapp_product"."id" = 5 LIMIT 21;


select "shopapp_productimages"."id",
       "shopapp_productimages"."product_id",
       "shopapp_productimages"."images",
       "shopapp_productimages"."description"
from "shopapp_productimages"
where "shopapp_productimages"."product_id" in (5);


SELECT "django_session"."session_key",
       "django_session"."session_data",
       "django_session"."expire_date"
FROM "django_session"
WHERE ("django_session"."expire_date" > '2023-09-17 16:10:21.325512'
AND "django_session"."session_key" = 'd3rouqjr1y5099z8ntmma55zrj4t4ac1')
LIMIT 21;


SELECT "auth_user"."id",
       "auth_user"."password",
       "auth_user"."last_login",
       "auth_user"."is_superuser",
       "auth_user"."username",
       "auth_user"."first_name",
       "auth_user"."last_name",
       "auth_user"."email",
       "auth_user"."is_staff",
       "auth_user"."is_active",
       "auth_user"."date_joined"
FROM "auth_user"
WHERE "auth_user"."id" = 2
LIMIT 21;


select "shopapp_order"."id",
       "shopapp_order"."delivery_address",
       "shopapp_order"."promocode",
       "shopapp_order"."created_at",
       "shopapp_order"."user_id",
       "shopapp_order"."receipt",
       "auth_user"."id",
       "auth_user"."password",
       "auth_user"."last_login",
       "auth_user"."is_superuser",
       "auth_user"."username",
       "auth_user"."first_name",
       "auth_user"."last_name",
       "auth_user"."email",
       "auth_user"."is_staff",
       "auth_user"."is_active",
       "auth_user"."date_joined"
from "shopapp_order"
inner join "auth_user"
on ("shopapp_order"."user_id" = "auth_user"."id");


SELECT ("shopapp_order_products"."order_id") AS "_prefetch_related_val_order_id",
        "shopapp_product"."id",
        "shopapp_product"."name",
        "shopapp_product"."description",
        "shopapp_product"."quantity",
        "shopapp_product"."price",
        "shopapp_product"."discount",
        "shopapp_product"."created_at",
        "shopapp_product"."created_by_id",
        "shopapp_product"."archived",
        "shopapp_product"."preview"
FROM "shopapp_product"
INNER JOIN "shopapp_order_products"
ON ("shopapp_product"."id" = "shopapp_order_products"."product_id")
WHERE "shopapp_order_products"."order_id" IN (1, 2, 3)
ORDER BY "shopapp_product"."name" ASC, "shopapp_product"."price" ASC;