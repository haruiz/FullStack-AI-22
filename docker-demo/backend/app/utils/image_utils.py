class ImageUtils:
    @staticmethod
    def human_readable_size(num: float, suffix: str = "B") -> str:
        """
        Convert a size in bytes to a human readable format
        :param num: size in bytes
        :param suffix: suffix to append to the size
        :return:
        """
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(num) < 1024.0:
                # return size in bytes
                return f"{num:3.1f}{unit}{suffix}"
            # convert to next unit
            num /= 1024.0
        # return size in yottabytes (YiB), a measure of theoretical storage
        # capacity and data volumes equal to 2 to the 80th power bytes
        return f"{num:.1f}Yi{suffix}"
