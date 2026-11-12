from hotglue_smoke_test.vcr.tap import VCRTapTestRunner


class Runner(VCRTapTestRunner):
    FILTER_HEADERS = [
        *VCRTapTestRunner.FILTER_HEADERS,
        "cookie",
        "cf-ray",
        "x-request-id",
    ]
    PRESERVE_KEYS = {
        "id",  # Product IDs are reused in child metafield request paths.
        "updatedAt",  # Product replication key and final bookmark.
    }

    def module(self) -> str:
        return "tap_lightspeed.tap"

    def launch(self):
        from tap_lightspeed.tap import TapLightspeed

        TapLightspeed.cli()


if __name__ == "__main__":
    Runner.main()
