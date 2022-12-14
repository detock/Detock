#pragma once

#include "common/types.h"

namespace slog {

class MetadataInitializer {
 public:
  virtual ~MetadataInitializer() = default;
  virtual Metadata Compute(const Key& key) = 0;
};

class SimpleMetadataInitializer : public MetadataInitializer {
 public:
  SimpleMetadataInitializer(uint32_t num_regions, uint32_t num_partitions);
  Metadata Compute(const Key& key) override;

 private:
  uint32_t num_regions_;
  uint32_t num_partitions_;
};

class SimpleMetadataInitializer2 : public MetadataInitializer {
 public:
  SimpleMetadataInitializer2(uint32_t num_regions, uint32_t num_partitions);
  Metadata Compute(const Key& key) override;

 private:
  uint32_t num_regions_;
  uint32_t num_partitions_;
};
class ConstantMetadataInitializer : public MetadataInitializer {
 public:
  ConstantMetadataInitializer(uint32_t home);
  Metadata Compute(const Key& key) override;

 private:
  uint32_t home_;
};

}  // namespace slog