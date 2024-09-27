"""Stream type classes for tap-lightspeed."""

from singer_sdk import typing as th

from tap_lightspeed.client import LightspeedStream

tax_rates = th.ObjectType(
    th.Property("name", th.StringType),
    th.Property("rate", th.NumberType),
    th.Property("amount", th.NumberType),
)

resources = th.ObjectType(
    th.Property(
        "resource",
        th.ObjectType(
            th.Property("id", th.IntegerType),
            th.Property("url", th.StringType),
            th.Property("link", th.StringType),
        ),
    )
)

option = th.ObjectType(
    th.Property("sortOrder", th.IntegerType),
    th.Property("id", th.IntegerType),
    th.Property("name", th.StringType),  
)

country = th.ObjectType(
    th.Property("id", th.IntegerType),
    th.Property("code", th.StringType),
    th.Property("code3", th.StringType),
    th.Property("title", th.StringType),
)

class ShopStream(LightspeedStream):
    """Define custom stream."""

    name = "shop"
    path = "/shop.json"
    primary_keys = ["id"]
    records_jsonpath = "$.shop"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("status", th.StringType),
        th.Property("isB2b", th.BooleanType),
        th.Property("isRetail", th.BooleanType),
        th.Property("subDomain", th.StringType),
        th.Property("mainDomain", th.StringType),
        th.Property("email", th.StringType),
        th.Property("phone", th.StringType),
        th.Property("fax", th.StringType),
        th.Property("street", th.StringType),
        th.Property("street2", th.StringType),
        th.Property("zipcode", th.StringType),
        th.Property("city", th.StringType),
        th.Property("region", th.StringType),
        th.Property("country", country),
        th.Property("vatNumber", th.StringType),
        th.Property("cocNumber", th.StringType),
        th.Property("industry", th.StringType),
        th.Property("currency", th.ObjectType(
            th.Property("shortcode", th.StringType),
            th.Property("symbol", th.StringType),
            th.Property("title", th.StringType),
            th.Property("isDefault", th.BooleanType),
            th.Property("currencyRate", th.StringType),
        )),
        th.Property("company", resources),
        th.Property("limits", resources),
        th.Property("javascript", resources),
        th.Property("website", resources),
        th.Property("scripts", resources),
        th.Property("metafields", resources),
    ).to_dict()


class OrdersStream(LightspeedStream):
    """Define custom stream."""

    name = "orders"
    path = "/orders.json"
    primary_keys = ["id"]
    records_jsonpath = "$.orders[*]"
    replication_key = "updatedAt"
    replication_filter_field = "updated_at_min"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("number", th.StringType),
        th.Property("status", th.StringType),
        th.Property("customStatusId", th.IntegerType),
        th.Property("channel", th.StringType),
        th.Property("remoteIp", th.StringType),
        th.Property("userAgent", th.StringType),
        th.Property("referralId", th.StringType),
        th.Property("priceCost", th.NumberType),
        th.Property("priceExcl", th.NumberType),
        th.Property("priceIncl", th.NumberType),
        th.Property("weight", th.IntegerType),
        th.Property("volume", th.IntegerType),
        th.Property("colli", th.IntegerType),
        th.Property("gender", th.StringType),
        th.Property("birthDate", th.DateTimeType),
        th.Property("nationalId", th.StringType),
        th.Property("email", th.StringType),
        th.Property("firstname", th.StringType),
        th.Property("middlename", th.StringType),
        th.Property("lastname", th.StringType),
        th.Property("phone", th.StringType),
        th.Property("mobile", th.StringType),
        th.Property("isCompany", th.BooleanType),
        th.Property("companyName", th.StringType),
        th.Property("companyCoCNumber", th.StringType),
        th.Property("companyVatNumber", th.StringType),
        th.Property("addressBillingName", th.StringType),
        th.Property("addressBillingStreet", th.StringType),
        th.Property("addressBillingStreet2", th.StringType),
        th.Property("addressBillingNumber", th.StringType),
        th.Property("addressBillingExtension", th.StringType),
        th.Property("addressBillingZipcode", th.StringType),
        th.Property("addressBillingCity", th.StringType),
        th.Property("addressBillingRegion", th.StringType),
        th.Property("addressBillingCountry", country),
        th.Property("addressShippingCompany", th.StringType),
        th.Property("addressShippingName", th.StringType),
        th.Property("addressShippingStreet", th.StringType),
        th.Property("addressShippingStreet2", th.StringType),
        th.Property("addressShippingNumber", th.BooleanType),
        th.Property("addressShippingExtension", th.StringType),
        th.Property("addressShippingZipcode", th.StringType),
        th.Property("addressShippingCity", th.StringType),
        th.Property("addressShippingRegion", th.StringType),
        th.Property("addressShippingCountry", country),
        th.Property("paymentId", th.StringType),
        th.Property("paymentStatus", th.StringType),
        th.Property("paymentIsPost", th.BooleanType),
        th.Property("paymentIsInvoiceExternal", th.BooleanType),
        th.Property("paymentTaxRate", th.NumberType),
        th.Property("paymentTaxRates", th.ArrayType(tax_rates)),
        th.Property("paymentBasePriceExcl", th.NumberType),
        th.Property("paymentBasePriceIncl", th.NumberType),
        th.Property("paymentPriceExcl", th.NumberType),
        th.Property("paymentPriceIncl", th.NumberType),
        th.Property("paymentTitle", th.StringType),
        th.Property("paymentData", th.CustomType({"type": ["object", "string", "array"]})),
        th.Property("shipmentId", th.StringType),
        th.Property("shipmentStatus", th.StringType),
        th.Property("shipmentIsCashOnDelivery", th.BooleanType),
        th.Property("shipmentIsPickup", th.BooleanType),
        th.Property("shipmentTaxRate", th.NumberType),
        th.Property("shipmentTaxRates", th.ArrayType(tax_rates)),
        th.Property("shipmentBasePriceExcl", th.NumberType),
        th.Property("shipmentBasePriceIncl", th.NumberType),
        th.Property("shipmentPriceExcl", th.NumberType),
        th.Property("shipmentPriceIncl", th.NumberType),
        th.Property("shipmentDiscountExcl", th.NumberType),
        th.Property("shipmentDiscountIncl", th.NumberType),
        th.Property("shipmentTitle", th.StringType),
        th.Property("shipmentData", th.CustomType({"type": ["object", "string", "array"]})),
        th.Property("shippingDate", th.DateTimeType),
        th.Property("taxRates", th.ArrayType(tax_rates)),
        th.Property("deliveryDate", th.DateTimeType),
        th.Property("isDiscounted", th.BooleanType),
        th.Property("discountType", th.StringType),
        th.Property("discountAmount", th.NumberType),
        th.Property("discountPercentage", th.NumberType),
        th.Property("discountCouponCode", th.StringType),
        th.Property("isNewCustomer", th.BooleanType),
        th.Property("comment", th.StringType),
        th.Property("memo", th.StringType),
        th.Property("doNotifyNew", th.BooleanType),
        th.Property("doNotifyReminder", th.BooleanType),
        th.Property("doNotifyCancelled", th.BooleanType),
        th.Property(
            "language",
            th.ObjectType(
                th.Property("locale", th.StringType),
                th.Property("id", th.IntegerType),
                th.Property("code", th.StringType),
                th.Property("title", th.StringType),
            ),
        ),
        th.Property("customer", resources),
        th.Property("invoices", resources),
        th.Property("shipments", resources),
        th.Property("products", resources),
        th.Property("metafields", resources),
        th.Property("quote", resources),
        th.Property("events", resources),
    ).to_dict()

    def get_child_context(self, record, context) -> dict:
        return {"order_id": record["id"]}


class OrderLinesStream(LightspeedStream):
    """Define custom stream."""

    name = "order_lines"
    path = "/orders/{order_id}/products.json"
    primary_keys = ["id"]
    parent_stream_type = OrdersStream
    records_jsonpath = "$.orderProducts[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("supplierTitle", th.StringType),
        th.Property("brandTitle", th.StringType),
        th.Property("productTitle", th.StringType),
        th.Property("variantTitle", th.StringType),
        th.Property("taxRate", th.NumberType),
        th.Property("quantityOrdered", th.IntegerType),
        th.Property("quantityInvoiced", th.IntegerType),
        th.Property("quantityShipped", th.IntegerType),
        th.Property("quantityRefunded", th.IntegerType),
        th.Property("quantityReturned", th.IntegerType),
        th.Property("articleCode", th.StringType),
        th.Property("ean", th.StringType),
        th.Property("sku", th.StringType),
        th.Property("weight", th.IntegerType),
        th.Property("volume", th.IntegerType),
        th.Property("colli", th.IntegerType),
        th.Property("sizeX", th.IntegerType),
        th.Property("sizeY", th.IntegerType),
        th.Property("sizeZ", th.IntegerType),
        th.Property("priceCost", th.NumberType),
        th.Property("customExcl", th.NumberType),
        th.Property("customIncl", th.NumberType),
        th.Property("basePriceExcl", th.NumberType),
        th.Property("basePriceIncl", th.NumberType),
        th.Property("priceExcl", th.NumberType),
        th.Property("priceIncl", th.NumberType),
        th.Property("discountExcl", th.NumberType),
        th.Property("discountIncl", th.NumberType),
        th.Property("customFields", th.CustomType({"type": ["array","object", "string"]})),
        th.Property("order_id", th.IntegerType),
        th.Property("product", resources),
        th.Property("variant", resources),
    ).to_dict()


class OrderMetafieldsStream(LightspeedStream):
    """Define custom stream."""

    name = "order_metafields"
    path = "/orders/{order_id}/metafields.json"
    parent_stream_type = OrdersStream
    records_jsonpath = "$.orderMetafields[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("key", th.StringType),
        th.Property("value", th.StringType),
        th.Property("order_id", th.IntegerType),
    ).to_dict()


class ShipmentsLinesStream(LightspeedStream):
    """Define custom stream."""

    name = "order_shipping_lines"
    path = "/shipments.json"
    primary_keys = ["id"]
    parent_stream_type = OrdersStream
    records_jsonpath = "$.shipments[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("number", th.StringType),
        th.Property("status", th.StringType),
        th.Property("trackingCode", th.StringType),
        th.Property("doNotifyShipped", th.BooleanType),
        th.Property("doNotifyReadyForPickup", th.BooleanType),
        th.Property("doNotifyTrackingCode", th.BooleanType),
        th.Property("totalWeight", th.IntegerType),
        th.Property("totalSizeX", th.IntegerType),
        th.Property("totalSizeY", th.IntegerType),
        th.Property("totalSizeZ", th.IntegerType),
        th.Property("order_id", th.IntegerType),
        th.Property("customer", resources),
        th.Property("order", resources),
        th.Property("products", resources),
        th.Property("metafields", resources),
        th.Property("events", resources),
    ).to_dict()

    def get_url_params(self, context, next_page_token):
        params = {"order": context.get("order_id")}
        params.update(super().get_url_params(context, next_page_token))
        return params


class ProductsStream(LightspeedStream):
    """Define custom stream."""

    name = "products"
    path = "/products.json"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    replication_filter_field = "updated_at_min"
    records_jsonpath = "$.products[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("isVisible", th.BooleanType),
        th.Property("visibility", th.StringType),
        th.Property("data01", th.StringType),
        th.Property("data02", th.StringType),
        th.Property("data03", th.StringType),
        th.Property("url", th.StringType),
        th.Property("title", th.StringType),
        th.Property("fulltitle", th.StringType),
        th.Property("description", th.StringType),
        th.Property("content", th.StringType),
        th.Property("set", th.CustomType({"type": ["object", "string"]})),
        th.Property("brand", resources),
        th.Property("categories", resources),
        th.Property("deliverydate", resources),
        th.Property("image", th.CustomType({"type": ["object", "string"]})),
        th.Property("images", th.CustomType({"type": ["object", "string"]})),
        th.Property("relations", resources),
        th.Property("metafields", resources),
        th.Property("reviews", resources),
        th.Property("type", resources),
        th.Property("attributes", resources),
        th.Property("supplier", resources),
        th.Property("tags", resources),
        th.Property("variants", resources),
        th.Property("movements", resources),
    ).to_dict()

    def get_child_context(self, record: dict, context) -> dict:
        return {"product_id": record["id"]}


class VariantsStream(LightspeedStream):
    """Define custom stream."""

    name = "variants"
    path = "/variants.json"
    primary_keys = ["id"]
    parent_stream_type = ProductsStream
    records_jsonpath = "$.variants[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("isDefault", th.BooleanType),
        th.Property("sortOrder", th.IntegerType),
        th.Property("articleCode", th.StringType),
        th.Property("ean", th.StringType),
        th.Property("sku", th.StringType),
        th.Property("hs", th.StringType),
        th.Property("unitPrice", th.NumberType),
        th.Property("unitUnit", th.StringType),
        th.Property("priceExcl", th.NumberType),
        th.Property("priceIncl", th.NumberType),
        th.Property("priceCost", th.NumberType),
        th.Property("oldPriceExcl", th.NumberType),
        th.Property("oldPriceIncl", th.NumberType),
        th.Property("stockTracking", th.StringType),  
        th.Property("stockLevel", th.NumberType),
        th.Property("stockAlert", th.NumberType),
        th.Property("stockMinimum", th.NumberType),
        th.Property("stockSold", th.NumberType),
        th.Property("stockBuyMininum", th.NumberType),
        th.Property("stockBuyMaximum", th.NumberType),
        th.Property("weight", th.NumberType),
        th.Property("weightValue", th.StringType),
        th.Property("weightUnit", th.StringType),
        th.Property("volume", th.NumberType),
        th.Property("volumeValue", th.NumberType),
        th.Property("volumeUnit", th.StringType),  
        th.Property("colli", th.NumberType),
        th.Property("sizeX", th.NumberType),
        th.Property("sizeY", th.NumberType),
        th.Property("sizeZ", th.NumberType),
        th.Property("sizeXValue", th.StringType),
        th.Property("sizeYValue", th.StringType),
        th.Property("sizeZValue", th.StringType),
        th.Property("sizeUnit", th.StringType),
        th.Property("matrix", th.StringType),
        th.Property("title", th.StringType),  
        th.Property("taxType", th.StringType),
        th.Property("image", th.CustomType({"type": ["object", "string"]})),
        th.Property("additionalcost", th.BooleanType),
        th.Property("options", th.ArrayType(
            th.ObjectType(
                th.Property("values", th.ArrayType(option)),
                th.Property("sortOrder", th.IntegerType),
                th.Property("id", th.IntegerType),
                th.Property("value", option),  
                th.Property("createdAt", th.DateTimeType),
                th.Property("updatedAt", th.DateTimeType),
                th.Property("name", th.StringType),
            )
        )),
        th.Property("product_id", th.IntegerType),
        th.Property("tax", resources),
        th.Property("product", resources),
    ).to_dict()

    def get_url_params(self, context, next_page_token):
        params = {"product": context.get("product_id")}
        params.update(super().get_url_params(context, next_page_token))
        return params
    

class ProductsImagesStream(LightspeedStream):
    """Define custom stream."""

    name = "products_images"
    path = "/products/{product_id}/images.json"
    primary_keys = ["id"]
    parent_stream_type = ProductsStream
    records_jsonpath = "$.productImages[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("sortOrder", th.IntegerType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("extension", th.StringType),
        th.Property("size", th.IntegerType),
        th.Property("title", th.StringType),
        th.Property("thumb", th.StringType),
        th.Property("src", th.StringType),
        th.Property("product_id", th.IntegerType),
    ).to_dict()


class ProductsMetafieldsStream(LightspeedStream):
    """Define custom stream."""

    name = "products_metafields"
    path = "/products/{product_id}/metafields.json"
    parent_stream_type = ProductsStream
    records_jsonpath = "$.productMetafields[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("key", th.StringType),
        th.Property("value", th.StringType),
        th.Property("product_id", th.IntegerType),
    ).to_dict()


class CategoriesStream(LightspeedStream):
    """Define custom stream."""

    name = "categories"
    path = "/categories.json"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    replication_filter_field = "updated_at_min"
    records_jsonpath = "$.categories[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("isVisible", th.BooleanType),
        th.Property("depth", th.IntegerType),
        th.Property("path", th.ArrayType(th.StringType)),
        th.Property("type", th.StringType),
        th.Property("sortOrder", th.IntegerType),
        th.Property("sorting", th.StringType),
        th.Property("url", th.StringType),
        th.Property("title", th.StringType),
        th.Property("fulltitle", th.StringType),
        th.Property("description", th.StringType),
        th.Property("content", th.StringType),
        th.Property("image", th.CustomType({"type": ["object", "string"]})),
        th.Property("parent", resources),
        th.Property("children", resources),
        th.Property("products", resources),
    ).to_dict()


class CategoriesProductStream(LightspeedStream):
    """Define custom stream."""

    name = "categories_product"
    path = "/categories/products.json"
    primary_keys = ["id"]
    records_jsonpath = "$.categoriesProducts[*]"
    parent_stream_type = ProductsStream
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("sortOrder", th.IntegerType),
        th.Property("product_id", th.IntegerType),
        th.Property("category", resources),
        th.Property("product", resources),
    ).to_dict()

    def get_url_params(self, context, next_page_token):
        params = {"product": context.get("product_id")}
        params.update(super().get_url_params(context, next_page_token))
        return params


class SuppliersStream(LightspeedStream):
    """Define custom stream."""

    name = "suppliers"
    path = "/suppliers.json"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    replication_filter_field = "updated_at_min"
    records_jsonpath = "$.suppliers[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("title", th.StringType),
        th.Property("attention_of", th.StringType),
        th.Property("street", th.StringType),
        th.Property("street2", th.StringType),
        th.Property("number", th.StringType),
        th.Property("extension", th.StringType),
        th.Property("zip_code", th.StringType),
        th.Property("city", th.StringType),
        th.Property("region", th.StringType),
        th.Property("country_id", country),
    ).to_dict()


class CustomersStream(LightspeedStream):
    """Define custom stream."""

    name = "customers"
    path = "/customers.json"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    replication_filter_field = "updated_at_min"
    records_jsonpath = "$.customers[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("lastOnlineAt", th.DateTimeType),
        th.Property("isConfirmed", th.BooleanType),
        th.Property("remoteIp", th.StringType),
        th.Property("userAgent", th.StringType),
        th.Property("referralId", th.StringType),
        th.Property("gender", th.StringType),
        th.Property("birthDate", th.StringType),
        th.Property("nationalId", th.StringType),
        th.Property("email", th.StringType),
        th.Property("firstname", th.StringType),
        th.Property("middlename", th.StringType),
        th.Property("lastname", th.StringType),
        th.Property("phone", th.StringType),
        th.Property("mobile", th.StringType),
        th.Property("isCompany", th.BooleanType),
        th.Property("companyName", th.StringType),
        th.Property("companyCoCNumber", th.StringType),
        th.Property("companyVatNumber", th.StringType),
        th.Property("addressBillingName", th.StringType),
        th.Property("addressBillingStreet", th.StringType),
        th.Property("addressBillingStreet2", th.StringType),
        th.Property("addressBillingNumber", th.StringType),
        th.Property("addressBillingExtension", th.StringType),
        th.Property("addressBillingZipcode", th.StringType),
        th.Property("addressBillingCity", th.BooleanType),
        th.Property("addressBillingRegion", th.StringType),
        th.Property("addressBillingCountry", country),
        th.Property("addressShippingCompany", th.StringType),
        th.Property("addressShippingName", th.StringType),
        th.Property("addressShippingStreet", th.StringType),
        th.Property("addressShippingStreet2", th.StringType),
        th.Property("addressShippingNumber", th.StringType),
        th.Property("addressShippingExtension", th.StringType),
        th.Property("addressShippingZipcode", th.StringType),
        th.Property("addressShippingCity", th.StringType),
        th.Property("addressShippingRegion", th.StringType),
        th.Property("addressShippingCountry", country),
        th.Property("memo", th.StringType),
        th.Property("doNotifyRegistered", th.BooleanType),
        th.Property("doNotifyConfirmed", th.BooleanType),
        th.Property("doNotifyPassword", th.BooleanType),
        th.Property("groups", resources),
        th.Property("invoices", resources),
        th.Property("orders", resources),
        th.Property("reviews", resources),
        th.Property("shipments", resources),
        th.Property("tickets", resources),
        th.Property("metafields", resources),
        th.Property("login", resources),
    ).to_dict()


class ReturnsStream(LightspeedStream):
    """Define custom stream."""

    name = "returns"
    path = "/returns.json"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    replication_filter_field = "updated_at_min"
    records_jsonpath = "$.returns[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("customerId", th.IntegerType),
        th.Property("orderId", th.IntegerType),
        th.Property("status", th.StringType),
        th.Property("numProducts", th.IntegerType),
        th.Property("priceExcl", th.NumberType),
        th.Property("priceIncl", th.NumberType),
        th.Property("isStockAdjusted", th.BooleanType),
        th.Property("returnReason", th.StringType),
        th.Property("returnAction", th.StringType),
        th.Property("customerComment", th.StringType),
        th.Property("staffNote", th.StringType),
        th.Property("mailMessage", th.StringType),
        th.Property("notifyStatus", th.BooleanType),
        th.Property(
            "orderProducts",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("quantity", th.IntegerType),
                )
            ),
        ),
    ).to_dict()
