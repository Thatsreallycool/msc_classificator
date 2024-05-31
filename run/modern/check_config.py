from zb_msc_classificator.config.definition import ConfigGenerate, ConfigClassify

test_gen = ConfigGenerate(training_source="disk")
print(f"Gen:{test_gen}")

test_cls = ConfigClassify(nr_msc_cutoff=5)
print(f"Cls:{test_cls}")
